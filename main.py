"""
FastAPI Backend for Market Merchant App
Main application entry point with all routes and middleware
"""

from fastapi import FastAPI, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import json
import uuid
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="Market Merchant API",
    description="Backend API for Market Merchant Dashboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Ensure all HTTP methods, including OPTIONS, are allowed
    allow_headers=["Authorization", "Content-Type", "*"],  # Explicitly allow Authorization and Content-Type headers
)

# Add a global exception handler for OPTIONS requests
@app.options("/{path:path}")
async def handle_options(path: str):
    """Handle OPTIONS requests for CORS preflight"""
    return {"message": "CORS preflight handled"}

# Add logging for requests and responses
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    if request.method in ["POST", "PUT"]:
        body = await request.body()
        logger.info(f"Request body: {body.decode('utf-8')}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Security
security = HTTPBearer()

# In-memory data store
class MemoryStore:
    def __init__(self):
        self.merchants = {}
        self.products = {}
        self.orders = {}
        self.offers = {}
        self.sessions = {}
        self.reviews = {}
        self._init_mock_data()
    
    def _init_mock_data(self):
        """Initialize with mock data matching React app expectations"""
        # Mock merchant
        self.merchants["merchant123"] = {
            "merchant_id": "merchant123",
            "business_name": "Fresh Market Store",
            "business_type": "grocery",
            "email": "merchant@freshmarket.com",
            "phone": "+91-9876543210",
            "address": "Shop 15, Main Market, Sector 17, Chandigarh",
            "latitude": 30.7333,
            "longitude": 76.7794,
            "subscription_plan": "premium",
            "shop_status": {
                "is_open": True,
                "accepting_orders": True,
                "reason": None
            },
            "created_at": "2024-01-15T10:00:00Z"
        }
        
        # Mock products
        self.products.update({
            "prod1": {
                "product_id": "prod1",
                "merchant_id": "merchant123",
                "name": "Fresh Red Apples",
                "category": "fruits",
                "subcategory": "seasonal",
                "brand": "Local Farm",
                "description": "Fresh red apples, perfect for snacking. Crisp and sweet variety.",
                "variants": [
                    {"id": "var1", "name": "1kg", "mrp": 150, "selling_price": 120, "stock_quantity": 50, "sku": "AP001"},
                    {"id": "var2", "name": "2kg", "mrp": 280, "selling_price": 220, "stock_quantity": 25, "sku": "AP002"}
                ],
                "images": ["https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=200&fit=crop"],
                "is_active": True,
                "weight": 1.0,
                "created_at": "2024-01-15T10:00:00Z"
            },
            "prod2": {
                "product_id": "prod2",
                "merchant_id": "merchant123",
                "name": "Organic Whole Milk",
                "category": "dairy",
                "subcategory": "organic",
                "brand": "Pure Dairy",
                "description": "Fresh organic milk from grass-fed cows. Rich in nutrients and taste.",
                "variants": [
                    {"id": "var3", "name": "1L", "mrp": 70, "selling_price": 60, "stock_quantity": 5, "sku": "MK001"},
                    {"id": "var4", "name": "500ml", "mrp": 40, "selling_price": 35, "stock_quantity": 15, "sku": "MK002"}
                ],
                "images": ["https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=200&fit=crop"],
                "is_active": True,
                "weight": 1.0,
                "created_at": "2024-01-15T11:00:00Z"
            },
            "prod3": {
                "product_id": "prod3",
                "merchant_id": "merchant123",
                "name": "Fresh White Bread",
                "category": "bakery",
                "subcategory": "daily",
                "brand": "Daily Bread",
                "description": "Freshly baked bread, made daily with premium flour.",
                "variants": [
                    {"id": "var5", "name": "500g", "mrp": 40, "selling_price": 35, "stock_quantity": 80, "sku": "BR001"}
                ],
                "images": ["https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300&h=200&fit=crop"],
                "is_active": True,
                "weight": 0.5,
                "created_at": "2024-01-15T12:00:00Z"
            }
        })
        
        # Mock orders
        self.orders.update({
            "ORD001": {
                "order_id": "ORD001",
                "merchant_id": "merchant123",
                "customer_name": "John Doe",
                "customer_phone": "+91-9876543210",
                "items": [
                    {"product_name": "Fresh Apples", "variant": "1kg", "quantity": 2, "unit_price": 120, "total_price": 240},
                    {"product_name": "Organic Milk", "variant": "1L", "quantity": 1, "unit_price": 60, "total_price": 60}
                ],
                "total_amount": 300.0,
                "status": "pending",
                "delivery_type": "delivery",
                "delivery_address": "123 Main St, Sector 17, Chandigarh",
                "created_at": "2024-01-15T10:30:00Z",
                "customer_notes": "Please deliver fresh items"
            },
            "ORD002": {
                "order_id": "ORD002",
                "merchant_id": "merchant123",
                "customer_name": "Jane Smith",
                "customer_phone": "+91-9876543211",
                "items": [
                    {"product_name": "Fresh Bread", "variant": "500g", "quantity": 2, "unit_price": 35, "total_price": 70},
                    {"product_name": "Premium Basmati Rice", "variant": "1kg", "quantity": 1, "unit_price": 150, "total_price": 150}
                ],
                "total_amount": 220.0,
                "status": "preparing",
                "delivery_type": "pickup",
                "created_at": "2024-01-15T11:15:00Z",
                "customer_notes": ""
            },
            "ORD003": {
                "order_id": "ORD003",
                "merchant_id": "merchant123",
                "customer_name": "Bob Johnson",
                "customer_phone": "+91-9876543212",
                "items": [
                    {"product_name": "Fresh Bread", "variant": "500g", "quantity": 1, "unit_price": 35, "total_price": 35}
                ],
                "total_amount": 125.0,
                "status": "ready",
                "delivery_type": "delivery",
                "delivery_address": "456 Park St, Sector 22, Chandigarh",
                "created_at": "2024-01-15T12:00:00Z",
                "customer_notes": ""
            }
        })
        
        # Mock offers
        self.offers.update({
            "off1": {
                "offer_id": "off1",
                "merchant_id": "merchant123",
                "name": "20% Off on Fruits",
                "description": "Get 20% discount on all fruit items",
                "type": "percentage",
                "level": "category",
                "discount_value": 20,
                "valid_from": "2024-01-15T00:00:00Z",
                "valid_till": "2024-01-31T23:59:59Z",
                "is_active": True,
                "usage_count": 15,
                "conditions": {"min_order_value": 100, "max_discount": 50},
                "applicable_categories": ["fruits"]
            },
            "off2": {
                "offer_id": "off2",
                "merchant_id": "merchant123",
                "name": "Buy 2 Get 1 Free",
                "description": "Buy 2 dairy products and get 1 free",
                "type": "buy_x_get_y",
                "level": "category",
                "discount_value": 0,
                "valid_from": "2024-01-15T00:00:00Z",
                "valid_till": "2024-02-15T23:59:59Z",
                "is_active": True,
                "usage_count": 8,
                "conditions": {"buy_quantity": 2, "get_quantity": 1},
                "applicable_categories": ["dairy"]
            }
        })

# Global memory store instance
memory_store = MemoryStore()

# Pydantic models
class GoogleAuthRequest(BaseModel):
    access_token: str

class AuthResponse(BaseModel):
    token: str
    merchant: Dict[str, Any]

class ShopStatusUpdate(BaseModel):
    is_open: bool
    accepting_orders: bool
    reason: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str

class ProductCreate(BaseModel):
    name: str
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    variants: List[Dict[str, Any]]
    images: List[str] = []
    weight: Optional[float] = None

class OfferCreate(BaseModel):
    name: str
    description: str
    type: str  # percentage, fixed_amount, buy_x_get_y
    level: str  # product, category, merchant
    discount_value: float
    valid_from: str
    valid_till: str
    conditions: Dict[str, Any] = {}
    applicable_categories: List[str] = []
    product_ids: List[str] = []

class ReviewCreate(BaseModel):
    customer_id: str
    order_id: str
    rating: int
    title: Optional[str] = None
    comment: Optional[str] = None
    images: List[str] = []
    shop_id: Optional[str] = None
    product_id: Optional[str] = None

# Authentication helper
def get_current_merchant(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract merchant ID from JWT token (simplified for demo)"""
    token = credentials.credentials
    
    # For demo, accept any token and return merchant123
    if token and token.startswith(('mock', 'demo')):
        return "merchant123"
    
    # In real implementation, decode JWT and extract merchant_id
    for session_id, session_data in memory_store.sessions.items():
        if session_data.get("token") == token:
            return session_data.get("merchant_id")
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Market Merchant API is running", "timestamp": datetime.now()}

@app.post("/auth/google", response_model=AuthResponse)
async def google_auth(auth_request: GoogleAuthRequest):
    logger.info(f"Received auth request with token: {auth_request.access_token}")

    if not auth_request.access_token:
        logger.warning("Access token missing in auth request")
        raise HTTPException(status_code=400, detail="Access token required")

    session_id = str(uuid.uuid4())
    token = f"demo-token-{session_id}"
    merchant_id = "merchant123"

    memory_store.sessions[session_id] = {
        "token": token,
        "merchant_id": merchant_id,
        "created_at": datetime.now().isoformat()
    }

    logger.info(f"Session created for merchant {merchant_id} with session_id {session_id}")

    merchant = memory_store.merchants.get(merchant_id)
    if not merchant:
        logger.error(f"Merchant {merchant_id} not found during auth")
        raise HTTPException(status_code=404, detail="Merchant not found")

    return AuthResponse(token=token, merchant=merchant)


@app.get("/dashboard")
async def get_dashboard(merchant_id: str = Depends(get_current_merchant)):
    """Get dashboard analytics data"""
    # Calculate dashboard metrics from orders
    merchant_orders = [o for o in memory_store.orders.values() if o["merchant_id"] == merchant_id]
    today = datetime.now().date()
    
    # Today's orders
    orders_today = len([o for o in merchant_orders if datetime.fromisoformat(o["created_at"].replace('Z', '+00:00')).date() == today])
    
    # Today's revenue
    revenue_today = sum([o["total_amount"] for o in merchant_orders if datetime.fromisoformat(o["created_at"].replace('Z', '+00:00')).date() == today])
    
    # Active offers
    merchant_offers = [o for o in memory_store.offers.values() if o["merchant_id"] == merchant_id and o["is_active"]]
    active_offers = len(merchant_offers)
    
    # Low stock products
    merchant_products = [p for p in memory_store.products.values() if p["merchant_id"] == merchant_id]
    low_stock_products = len([p for p in merchant_products if any(v["stock_quantity"] < 10 for v in p["variants"])])
    
    # Top products (mock calculation)
    top_products = [
        {"name": "Fresh Apples", "sales": 45, "revenue": 2250},
        {"name": "Organic Milk", "sales": 32, "revenue": 1920},
        {"name": "Fresh Bread", "sales": 28, "revenue": 980}
    ]
    
    # Recent orders
    recent_orders = sorted(merchant_orders, key=lambda x: x["created_at"], reverse=True)[:5]
    formatted_recent_orders = []
    for order in recent_orders:
        formatted_recent_orders.append({
            "order_id": order["order_id"],
            "customer": order["customer_name"],
            "amount": order["total_amount"],
            "status": order["status"],
            "items": len(order["items"])
        })
    
    return {
        "orders_today": orders_today,
        "revenue_today": revenue_today,
        "active_offers": active_offers,
        "low_stock_products": low_stock_products,
        "total_products": len(merchant_products),
        "pending_orders": len([o for o in merchant_orders if o["status"] == "pending"]),
        "top_products": top_products,
        "recent_orders": formatted_recent_orders
    }

@app.get("/merchants/profile")
async def get_merchant_profile(merchant_id: str = Depends(get_current_merchant)):
    """Get merchant profile information"""
    merchant = memory_store.merchants.get(merchant_id)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant

@app.put("/merchants/profile")
async def update_merchant_profile(profile_data: Dict[str, Any], merchant_id: str = Depends(get_current_merchant)):
    """Update merchant profile information"""
    if merchant_id not in memory_store.merchants:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    # Update merchant data
    memory_store.merchants[merchant_id].update(profile_data)
    memory_store.merchants[merchant_id]["updated_at"] = datetime.now().isoformat()
    
    return memory_store.merchants[merchant_id]

@app.get("/merchants/shop-status")
async def get_shop_status(merchant_id: str = Depends(get_current_merchant)):
    """Get shop operational status"""
    merchant = memory_store.merchants.get(merchant_id)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant["shop_status"]

@app.put("/merchants/shop-status")
async def update_shop_status(status_data: ShopStatusUpdate, merchant_id: str = Depends(get_current_merchant)):
    """Update shop operational status"""
    if merchant_id not in memory_store.merchants:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    memory_store.merchants[merchant_id]["shop_status"] = status_data.dict()
    return memory_store.merchants[merchant_id]["shop_status"]

@app.get("/products")
async def get_products(merchant_id: str = Depends(get_current_merchant), category: Optional[str] = None):
    """Get merchant's products with optional category filter"""
    logger.info(f"Fetching products for merchant_id: {merchant_id}, category: {category}")
    
    merchant_products = [p for p in memory_store.products.values() if p["merchant_id"] == merchant_id]
    
    if category:
        merchant_products = [p for p in merchant_products if p["category"] == category]
        logger.info(f"Filtered products by category: {category}, count: {len(merchant_products)}")
    
    logger.info(f"Total products returned: {len(merchant_products)}")
    return merchant_products

@app.post("/products")
async def create_product(product_data: ProductCreate, merchant_id: str = Depends(get_current_merchant)):
    """Create a new product"""
    product_id = f"prod_{uuid.uuid4().hex[:8]}"
    
    new_product = {
        "product_id": product_id,
        "merchant_id": merchant_id,
        **product_data.dict(),
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "offers": []
    }
    
    memory_store.products[product_id] = new_product
    return new_product

@app.get("/products/{product_id}")
async def get_product(product_id: str, merchant_id: str = Depends(get_current_merchant)):
    """Get specific product details"""
    product = memory_store.products.get(product_id)
    if not product or product["merchant_id"] != merchant_id:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}")
async def update_product(product_id: str, product_data: Dict[str, Any], merchant_id: str = Depends(get_current_merchant)):
    """Update product information"""
    if product_id not in memory_store.products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = memory_store.products[product_id]
    if product["merchant_id"] != merchant_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    
    memory_store.products[product_id].update(product_data)
    memory_store.products[product_id]["updated_at"] = datetime.now().isoformat()
    
    return memory_store.products[product_id]

@app.delete("/products/{product_id}")
async def delete_product(product_id: str, merchant_id: str = Depends(get_current_merchant)):
    """Delete a product"""
    if product_id not in memory_store.products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = memory_store.products[product_id]
    if product["merchant_id"] != merchant_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    
    del memory_store.products[product_id]
    return {"message": "Product deleted successfully"}

@app.get("/orders")
async def get_orders(merchant_id: str = Depends(get_current_merchant), status: Optional[str] = None):
    """Get merchant's orders with optional status filter"""
    merchant_orders = [o for o in memory_store.orders.values() if o["merchant_id"] == merchant_id]
    
    if status:
        merchant_orders = [o for o in merchant_orders if o["status"] == status]
    
    # Sort by creation date (newest first)
    merchant_orders.sort(key=lambda x: x["created_at"], reverse=True)
    return merchant_orders

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status_data: OrderStatusUpdate, merchant_id: str = Depends(get_current_merchant)):
    """Update order status"""
    if order_id not in memory_store.orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = memory_store.orders[order_id]
    if order["merchant_id"] != merchant_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    
    memory_store.orders[order_id]["status"] = status_data.status
    memory_store.orders[order_id]["updated_at"] = datetime.now().isoformat()
    
    return memory_store.orders[order_id]

@app.get("/offers")
async def get_offers(merchant_id: str = Depends(get_current_merchant)):
    """Get merchant's offers"""
    merchant_offers = [o for o in memory_store.offers.values() if o["merchant_id"] == merchant_id]
    return merchant_offers

@app.post("/offers")
async def create_offer(offer_data: OfferCreate, merchant_id: str = Depends(get_current_merchant)):
    """Create a new offer (supports product-level offers)"""
    offer_id = f"off_{uuid.uuid4().hex[:8]}"
    new_offer = {
        "offer_id": offer_id,
        "merchant_id": merchant_id,
        **offer_data.dict(),
        "is_active": True,
        "usage_count": 0,
        "created_at": datetime.now().isoformat()
    }
    memory_store.offers[offer_id] = new_offer
    # Attach offer to products if product_ids specified
    for pid in offer_data.product_ids:
        if pid in memory_store.products:
            memory_store.products[pid].setdefault("offers", []).append(offer_id)
    return new_offer

@app.put("/offers/{offer_id}")
async def update_offer(offer_id: str, offer_data: Dict[str, Any], merchant_id: str = Depends(get_current_merchant)):
    """Update offer information"""
    if offer_id not in memory_store.offers:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    offer = memory_store.offers[offer_id]
    if offer["merchant_id"] != merchant_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this offer")
    
    memory_store.offers[offer_id].update(offer_data)
    memory_store.offers[offer_id]["updated_at"] = datetime.now().isoformat()
    
    return memory_store.offers[offer_id]

@app.delete("/offers/{offer_id}")
async def delete_offer(offer_id: str, merchant_id: str = Depends(get_current_merchant)):
    """Delete an offer"""
    if offer_id not in memory_store.offers:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    offer = memory_store.offers[offer_id]
    if offer["merchant_id"] != merchant_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this offer")
    
    del memory_store.offers[offer_id]
    return {"message": "Offer deleted successfully"}

# In-memory reviews store
if not hasattr(memory_store, "reviews"):
    memory_store.reviews = {}

def get_current_customer(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    # For demo, accept any token and return customer123
    if token and token.startswith(("mock", "demo")):
        return "customer123"
    # Real implementation: decode JWT and extract customer_id
    for session_id, session_data in memory_store.sessions.items():
        if session_data.get("token") == token:
            return session_data.get("customer_id", "customer123")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.post("/reviews")
async def add_review(review: ReviewCreate = Body(...), customer_id: str = Depends(get_current_customer)):
    """Add a review for a product or shop (customer only)"""
    review_id = f"rev_{uuid.uuid4().hex[:8]}"
    review_dict = review.dict()
    review_dict["review_id"] = review_id
    review_dict["customer_id"] = customer_id
    review_dict["created_at"] = datetime.now().isoformat()
    review_dict["is_verified"] = True
    review_dict["is_approved"] = True
    memory_store.reviews[review_id] = review_dict
    # Update product/shop review stats
    if review.product_id and review.product_id in memory_store.products:
        p = memory_store.products[review.product_id]
        p["total_reviews"] = p.get("total_reviews", 0) + 1
        p["rating"] = round(((p.get("rating", 0) * (p["total_reviews"] - 1)) + review.rating) / p["total_reviews"], 2)
    if review.shop_id and review.shop_id in memory_store.merchants:
        s = memory_store.merchants[review.shop_id]
        s["total_reviews"] = s.get("total_reviews", 0) + 1
        s["rating"] = round(((s.get("rating", 0) * (s["total_reviews"] - 1)) + review.rating) / s["total_reviews"], 2)
    return review_dict

@app.get("/reviews")
async def get_reviews(product_id: Optional[str] = None, shop_id: Optional[str] = None):
    """List reviews for a product or shop"""
    reviews = list(memory_store.reviews.values())
    if product_id:
        reviews = [r for r in reviews if r.get("product_id") == product_id]
    if shop_id:
        reviews = [r for r in reviews if r.get("shop_id") == shop_id]
    return reviews

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
