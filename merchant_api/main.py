"""
Merchant API - FastAPI backend for merchant app
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid
import logging

from shared.auth.google_auth import google_auth_service
from shared.database.dynamodb import db_service
from shared.models.base import (
    BaseUser, Shop, Product, Order, Review, 
    UserRole, OrderStatus, ShopStatus
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Merchant API",
    description="Backend API for Merchant App",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Dependency to get current merchant
async def get_current_merchant(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current authenticated merchant"""
    try:
        user_data = google_auth_service.verify_jwt_token(credentials.credentials)
        user = await db_service.get_user(user_data["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user["role"] != UserRole.MERCHANT:
            raise HTTPException(status_code=403, detail="Access denied. Merchant role required.")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")

# Pydantic models for requests
from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    access_token: str

class AuthResponse(BaseModel):
    token: str
    user: Dict[str, Any]

class ShopCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float
    phone: str
    email: Optional[str] = None
    website: Optional[str] = None
    operating_hours: Dict[str, Dict[str, str]]
    delivery_radius: float = 5.0
    minimum_order: float = 0.0
    delivery_fee: float = 0.0

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    operating_hours: Optional[Dict[str, Dict[str, str]]] = None
    delivery_radius: Optional[float] = None
    minimum_order: Optional[float] = None
    delivery_fee: Optional[float] = None

class ShopStatusUpdate(BaseModel):
    is_open: bool
    accepting_orders: bool
    reason: Optional[str] = None

class ProductVariantCreate(BaseModel):
    name: str
    sku: str
    mrp: float
    selling_price: float
    stock_quantity: int
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, float]] = None

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    images: List[str] = []
    variants: List[ProductVariantCreate]

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    merchant_notes: Optional[str] = None

# Authentication routes
@app.post("/auth/google", response_model=AuthResponse)
async def google_auth(auth_request: GoogleAuthRequest):
    """Authenticate merchant with Google OAuth"""
    try:
        auth_result = await google_auth_service.authenticate_user(auth_request.access_token)
        
        # Check if user exists in database
        user = await db_service.get_user(auth_result["user"]["user_id"])
        if not user:
            # Create new user with merchant role
            auth_result["user"]["role"] = UserRole.MERCHANT
            user_model = BaseUser(**auth_result["user"])
            user = await db_service.create_user(user_model)
        elif user["role"] != UserRole.MERCHANT:
            # Update role to merchant if needed
            await db_service.update_user(user["user_id"], {"role": UserRole.MERCHANT})
            user["role"] = UserRole.MERCHANT
        
        return AuthResponse(
            token=auth_result["token"],
            user=user
        )
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# Dashboard routes
@app.get("/dashboard")
async def get_dashboard(current_merchant: Dict = Depends(get_current_merchant)):
    """Get merchant dashboard data"""
    try:
        merchant_id = current_merchant["user_id"]
        
        # Get merchant's shops
        shops = await db_service.get_shops_by_merchant(merchant_id)
        
        # Get recent orders across all shops
        all_orders = []
        for shop in shops:
            shop_orders = await db_service.get_orders_by_shop(shop["shop_id"])
            all_orders.extend(shop_orders)
        
        # Sort orders by creation date
        all_orders.sort(key=lambda x: x["created_at"], reverse=True)
        recent_orders = all_orders[:10]  # Last 10 orders
        
        # Calculate statistics
        total_orders = len(all_orders)
        pending_orders = len([o for o in all_orders if o["status"] == OrderStatus.PENDING])
        total_revenue = sum(o["total_amount"] for o in all_orders if o["status"] == OrderStatus.DELIVERED)
        
        return {
            "shops": shops,
            "recent_orders": recent_orders,
            "statistics": {
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "total_revenue": total_revenue,
                "total_shops": len(shops)
            }
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard")

# Shop routes
@app.get("/shops")
async def get_merchant_shops(current_merchant: Dict = Depends(get_current_merchant)):
    """Get all shops for the merchant"""
    try:
        shops = await db_service.get_shops_by_merchant(current_merchant["user_id"])
        return {"shops": shops}
    except Exception as e:
        logger.error(f"Error fetching shops: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch shops")

@app.post("/shops")
async def create_shop(
    shop_data: ShopCreate,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Create a new shop"""
    try:
        shop = Shop(
            shop_id=str(uuid.uuid4()),
            merchant_id=current_merchant["user_id"],
            **shop_data.dict()
        )
        
        created_shop = await db_service.create_shop(shop)
        return created_shop
    except Exception as e:
        logger.error(f"Error creating shop: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create shop")

@app.get("/shops/{shop_id}")
async def get_shop(
    shop_id: str,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Get shop details"""
    try:
        shop = await db_service.get_shop(shop_id)
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        if shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return shop
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching shop: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch shop")

@app.put("/shops/{shop_id}")
async def update_shop(
    shop_id: str,
    shop_data: ShopUpdate,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Update shop details"""
    try:
        # Verify shop ownership
        shop = await db_service.get_shop(shop_id)
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        # Update shop
        updates = {k: v for k, v in shop_data.dict().items() if v is not None}
        updates["updated_at"] = datetime.utcnow()
        
        updated_shop = await db_service.update_shop(shop_id, updates)
        return updated_shop
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating shop: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update shop")

@app.put("/shops/{shop_id}/status")
async def update_shop_status(
    shop_id: str,
    status_data: ShopStatusUpdate,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Update shop open/close status"""
    try:
        # Verify shop ownership
        shop = await db_service.get_shop(shop_id)
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        updates = {
            "is_open": status_data.is_open,
            "accepting_orders": status_data.accepting_orders,
            "updated_at": datetime.utcnow()
        }
        
        if status_data.reason:
            updates["status_reason"] = status_data.reason
        
        updated_shop = await db_service.update_shop(shop_id, updates)
        return updated_shop
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating shop status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update shop status")

# Product routes
@app.get("/shops/{shop_id}/products")
async def get_shop_products(
    shop_id: str,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Get all products for a shop"""
    try:
        # Verify shop ownership
        shop = await db_service.get_shop(shop_id)
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        products = await db_service.get_products_by_shop(shop_id)
        return {"products": products}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@app.post("/shops/{shop_id}/products")
async def create_product(
    shop_id: str,
    product_data: ProductCreate,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Create a new product"""
    try:
        # Verify shop ownership
        shop = await db_service.get_shop(shop_id)
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        # Convert variants
        variants = []
        for var_data in product_data.variants:
            variant = {
                "variant_id": str(uuid.uuid4()),
                **var_data.dict()
            }
            variants.append(variant)
        
        product = Product(
            product_id=str(uuid.uuid4()),
            shop_id=shop_id,
            variants=variants,
            **{k: v for k, v in product_data.dict().items() if k != "variants"}
        )
        
        created_product = await db_service.create_product(product)
        return created_product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@app.get("/products/{product_id}")
async def get_product(
    product_id: str,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Get product details"""
    try:
        product = await db_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Verify shop ownership
        shop = await db_service.get_shop(product["shop_id"])
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")

@app.put("/products/{product_id}")
async def update_product(
    product_id: str,
    updates: Dict[str, Any],
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Update product details"""
    try:
        # Verify product ownership
        product = await db_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        shop = await db_service.get_shop(product["shop_id"])
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # This would need to be implemented in the database service
        # For now, return the product with updates
        product.update(updates)
        product["updated_at"] = datetime.utcnow()
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update product")

# Order routes
@app.get("/shops/{shop_id}/orders")
async def get_shop_orders(
    shop_id: str,
    status: Optional[OrderStatus] = None,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Get orders for a shop"""
    try:
        # Verify shop ownership
        shop = await db_service.get_shop(shop_id)
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        orders = await db_service.get_orders_by_shop(shop_id, status)
        return {"orders": orders}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

@app.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Update order status"""
    try:
        # Get order and verify shop ownership
        order = await db_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        shop = await db_service.get_shop(order["shop_id"])
        if not shop or shop["merchant_id"] != current_merchant["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Update order status
        updates = {
            "status": status_data.status,
            "updated_at": datetime.utcnow()
        }
        
        if status_data.merchant_notes:
            updates["merchant_notes"] = status_data.merchant_notes
        
        updated_order = await db_service.update_order_status(order_id, status_data.status)
        return updated_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update order status")

# Profile routes
@app.get("/profile")
async def get_profile(current_merchant: Dict = Depends(get_current_merchant)):
    """Get merchant profile"""
    return current_merchant

@app.put("/profile")
async def update_profile(
    updates: Dict[str, Any],
    current_merchant: Dict = Depends(get_current_merchant)
):
    """Update merchant profile"""
    try:
        updated_user = await db_service.update_user(current_merchant["user_id"], updates)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 