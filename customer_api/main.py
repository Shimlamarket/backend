"""
Customer API - FastAPI backend for customer app
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
    BaseUser, Shop, Product, Order, Review, Address, 
    UserRole, OrderStatus, DeliveryType
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Customer API",
    description="Backend API for Customer App",
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

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current authenticated user"""
    try:
        user_data = google_auth_service.verify_jwt_token(credentials.credentials)
        user = await db_service.get_user(user_data["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
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

class AddressCreate(BaseModel):
    label: str
    street_address: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False

class CartItem(BaseModel):
    product_id: str
    variant_id: str
    quantity: int

class OrderCreate(BaseModel):
    shop_id: str
    items: List[CartItem]
    delivery_type: DeliveryType
    delivery_address: Optional[str] = None
    customer_notes: Optional[str] = None

class ReviewCreate(BaseModel):
    shop_id: Optional[str] = None
    product_id: Optional[str] = None
    order_id: str
    rating: int
    title: Optional[str] = None
    comment: Optional[str] = None

# Authentication routes
@app.post("/auth/google", response_model=AuthResponse)
async def google_auth(auth_request: GoogleAuthRequest):
    """Authenticate user with Google OAuth"""
    try:
        auth_result = await google_auth_service.authenticate_user(auth_request.access_token)
        
        # Check if user exists in database
        user = await db_service.get_user(auth_result["user"]["user_id"])
        if not user:
            # Create new user
            user_model = BaseUser(**auth_result["user"])
            user = await db_service.create_user(user_model)
        
        return AuthResponse(
            token=auth_result["token"],
            user=user
        )
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# Shop routes
@app.get("/shops")
async def get_shops(
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_open: Optional[bool] = None
):
    """Get approved shops with optional filters"""
    try:
        shops = await db_service.get_approved_shops(category)
        
        # Apply additional filters
        if search:
            shops = [s for s in shops if search.lower() in s["name"].lower()]
        
        if is_open is not None:
            shops = [s for s in shops if s["is_open"] == is_open]
        
        return {"shops": shops}
    except Exception as e:
        logger.error(f"Error fetching shops: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch shops")

@app.get("/shops/{shop_id}")
async def get_shop(shop_id: str):
    """Get shop details by ID"""
    try:
        shop = await db_service.get_shop(shop_id)
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        if shop["status"] != "approved":
            raise HTTPException(status_code=404, detail="Shop not found")
        
        return shop
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching shop: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch shop")

# Product routes
@app.get("/shops/{shop_id}/products")
async def get_shop_products(shop_id: str, category: Optional[str] = None):
    """Get products for a specific shop"""
    try:
        # Verify shop exists and is approved
        shop = await db_service.get_shop(shop_id)
        if not shop or shop["status"] != "approved":
            raise HTTPException(status_code=404, detail="Shop not found")
        
        products = await db_service.get_products_by_shop(shop_id)
        
        # Filter by category if provided
        if category:
            products = [p for p in products if p["category"] == category]
        
        return {"products": products}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get product details by ID"""
    try:
        product = await db_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")

# Address routes
@app.get("/addresses")
async def get_addresses(current_user: Dict = Depends(get_current_user)):
    """Get user addresses"""
    try:
        # This would need to be implemented in the database service
        # For now, return empty list
        return {"addresses": []}
    except Exception as e:
        logger.error(f"Error fetching addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch addresses")

@app.post("/addresses")
async def create_address(
    address_data: AddressCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new address for the user"""
    try:
        address = Address(
            address_id=str(uuid.uuid4()),
            user_id=current_user["user_id"],
            **address_data.dict()
        )
        
        # This would need to be implemented in the database service
        # For now, return the address data
        return address.dict()
    except Exception as e:
        logger.error(f"Error creating address: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create address")

# Order routes
@app.post("/orders")
async def create_order(
    order_data: OrderCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new order"""
    try:
        # Validate shop exists and is accepting orders
        shop = await db_service.get_shop(order_data.shop_id)
        if not shop or shop["status"] != "approved":
            raise HTTPException(status_code=404, detail="Shop not found")
        
        if not shop["accepting_orders"]:
            raise HTTPException(status_code=400, detail="Shop is not accepting orders")
        
        # Calculate order totals
        items = []
        subtotal = 0.0
        
        for cart_item in order_data.items:
            product = await db_service.get_product(cart_item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {cart_item.product_id} not found")
            
            # Find the variant
            variant = next((v for v in product["variants"] if v["variant_id"] == cart_item.variant_id), None)
            if not variant:
                raise HTTPException(status_code=404, detail=f"Variant {cart_item.variant_id} not found")
            
            if variant["stock_quantity"] < cart_item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product['name']}")
            
            item_total = variant["selling_price"] * cart_item.quantity
            subtotal += item_total
            
            items.append({
                "item_id": str(uuid.uuid4()),
                "product_id": cart_item.product_id,
                "variant_id": cart_item.variant_id,
                "product_name": product["name"],
                "variant_name": variant["name"],
                "quantity": cart_item.quantity,
                "unit_price": variant["selling_price"],
                "total_price": item_total
            })
        
        # Calculate delivery fee
        delivery_fee = shop["delivery_fee"] if order_data.delivery_type == DeliveryType.DELIVERY else 0.0
        total_amount = subtotal + delivery_fee
        
        # Create order
        order = Order(
            order_id=f"ORD{str(uuid.uuid4())[:8].upper()}",
            customer_id=current_user["user_id"],
            shop_id=order_data.shop_id,
            items=items,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            delivery_type=order_data.delivery_type,
            delivery_address=order_data.delivery_address,
            customer_notes=order_data.customer_notes
        )
        
        created_order = await db_service.create_order(order)
        return created_order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create order")

@app.get("/orders")
async def get_orders(current_user: Dict = Depends(get_current_user)):
    """Get user's order history"""
    try:
        orders = await db_service.get_orders_by_customer(current_user["user_id"])
        return {"orders": orders}
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

@app.get("/orders/{order_id}")
async def get_order(order_id: str, current_user: Dict = Depends(get_current_user)):
    """Get specific order details"""
    try:
        order = await db_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order["customer_id"] != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")

# Review routes
@app.post("/reviews")
async def create_review(
    review_data: ReviewCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new review"""
    try:
        # Validate order exists and belongs to user
        order = await db_service.get_order(review_data.order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order["customer_id"] != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if order is delivered
        if order["status"] != OrderStatus.DELIVERED:
            raise HTTPException(status_code=400, detail="Can only review delivered orders")
        
        review = Review(
            review_id=str(uuid.uuid4()),
            customer_id=current_user["user_id"],
            shop_id=review_data.shop_id,
            product_id=review_data.product_id,
            order_id=review_data.order_id,
            rating=review_data.rating,
            title=review_data.title,
            comment=review_data.comment,
            is_verified=True
        )
        
        # This would need to be implemented in the database service
        # For now, return the review data
        return review.dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating review: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create review")

# Profile routes
@app.get("/profile")
async def get_profile(current_user: Dict = Depends(get_current_user)):
    """Get user profile"""
    return current_user

@app.put("/profile")
async def update_profile(
    updates: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        updated_user = await db_service.update_user(current_user["user_id"], updates)
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
    uvicorn.run(app, host="0.0.0.0", port=8001) 