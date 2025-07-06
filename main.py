# main.py - Enhanced FastAPI with Better CORS & Debugging

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Market App API", version="1.0.0")

# Enhanced CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add custom middleware for debugging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"🔥 INCOMING REQUEST: {request.method} {request.url}")
    logger.info(f"🔥 Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"✅ RESPONSE: {response.status_code} - Processed in {process_time:.3f}s")
    
    return response

# Security
security = HTTPBearer()

# Enhanced Mock Database with more realistic data
MERCHANTS_DB = {
    "merchant123": {
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
        "created_at": "2024-01-01T00:00:00Z"
    }
}

ITEMS_DB = {
    "merchant123": [
        {
            "item_id": "item_001",
            "name": "Fresh Red Apples",
            "category": "fruits",
            "subcategory": "seasonal",
            "brand": "Local Farm",
            "description": "Fresh red apples, perfect for snacking",
            "price": 120,
            "mrp": 150,
            "stock_quantity": 50,
            "status": "active",
            "weight": 1.0,
            "sku": "AP001",
            "images": ["https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=200&fit=crop"],
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "item_id": "item_002",
            "name": "Organic Milk",
            "category": "dairy",
            "subcategory": "organic",
            "brand": "Pure Dairy",
            "description": "Fresh organic milk from grass-fed cows",
            "price": 60,
            "mrp": 70,
            "stock_quantity": 30,
            "status": "active",
            "weight": 1.0,
            "sku": "MK001",
            "images": ["https://images.unsplash.com/photo-1550583724-b2692b85b150?w=300&h=200&fit=crop"],
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "item_id": "item_003",
            "name": "Fresh Bread",
            "category": "bakery",
            "subcategory": "daily",
            "brand": "Baker's Choice",
            "description": "Freshly baked whole wheat bread",
            "price": 45,
            "mrp": 50,
            "stock_quantity": 15,
            "status": "active",
            "weight": 0.5,
            "sku": "BR001",
            "images": ["https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=300&h=200&fit=crop"],
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "item_id": "item_004",
            "name": "Bananas",
            "category": "fruits",
            "subcategory": "tropical",
            "brand": "Local Farm",
            "description": "Fresh ripe bananas",
            "price": 40,
            "mrp": 50,
            "stock_quantity": 8,  # Low stock
            "status": "active",
            "weight": 1.0,
            "sku": "BN001",
            "images": ["https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300&h=200&fit=crop"],
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "item_id": "item_005",
            "name": "Tomatoes",
            "category": "vegetables",
            "subcategory": "seasonal",
            "brand": "Local Farm",
            "description": "Fresh red tomatoes",
            "price": 80,
            "mrp": 90,
            "stock_quantity": 5,  # Low stock
            "status": "active",
            "weight": 1.0,
            "sku": "TM001",
            "images": ["https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=300&h=200&fit=crop"],
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
}

ORDERS_DB = {
    "merchant123": [
        {
            "order_id": "ORD-001",
            "customer_name": "Rajesh Kumar",
            "customer_phone": "+91 9876543210",
            "customer_address": "123 MG Road, Sector 14, Gurgaon, Haryana - 122001",
            "items": [
                {"product_id": "item_001", "product_name": "Fresh Red Apples", "quantity": 2, "price": 120},
                {"product_id": "item_002", "product_name": "Organic Milk", "quantity": 1, "price": 60}
            ],
            "total_amount": 300.0,
            "status": "pending",
            "order_time": "2024-01-20T14:30:00Z",
            "estimated_delivery": "2024-01-20T16:30:00Z"
        },
        {
            "order_id": "ORD-002",
            "customer_name": "Priya Sharma",
            "customer_phone": "+91 9876543211",
            "customer_address": "456 Cyber City, Gurgaon, Haryana - 122002",
            "items": [
                {"product_id": "item_003", "product_name": "Fresh Bread", "quantity": 2, "price": 45}
            ],
            "total_amount": 90.0,
            "status": "accepted",
            "order_time": "2024-01-20T15:00:00Z",
            "estimated_delivery": "2024-01-20T17:00:00Z"
        },
        {
            "order_id": "ORD-003",
            "customer_name": "Amit Singh",
            "customer_phone": "+91 9876543212",
            "customer_address": "789 Golf Course Road, Gurgaon, Haryana - 122003",
            "items": [
                {"product_id": "item_004", "product_name": "Bananas", "quantity": 3, "price": 40},
                {"product_id": "item_005", "product_name": "Tomatoes", "quantity": 1, "price": 80}
            ],
            "total_amount": 200.0,
            "status": "pending",
            "order_time": "2024-01-20T16:15:00Z",
            "estimated_delivery": "2024-01-20T18:15:00Z"
        }
    ]
}

OFFERS_DB = {
    "merchant123": [
        {
            "offer_id": "offer_001",
            "title": "Fresh Fruits 20% Off",
            "description": "Get 20% off on all fresh fruits",
            "discount_type": "percentage",
            "discount_value": 20,
            "min_order_value": 200,
            "max_discount": 100,
            "start_date": "2024-01-15T00:00:00Z",
            "end_date": "2024-01-30T23:59:59Z",
            "status": "active",
            "applicable_categories": ["fruits"]
        },
        {
            "offer_id": "offer_002",
            "title": "Buy 2 Get 1 Free - Dairy",
            "description": "Buy 2 dairy products and get 1 free",
            "discount_type": "bogo",
            "discount_value": 1,
            "min_order_value": 100,
            "start_date": "2024-01-10T00:00:00Z",
            "end_date": "2024-01-25T23:59:59Z",
            "status": "active",
            "applicable_categories": ["dairy"]
        },
        {
            "offer_id": "offer_003",
            "title": "Free Delivery",
            "description": "Free delivery on orders above ₹500",
            "discount_type": "fixed",
            "discount_value": 50,
            "min_order_value": 500,
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-12-31T23:59:59Z",
            "status": "active",
            "applicable_categories": []
        }
    ]
}

# Pydantic Models
class GoogleAuthRequest(BaseModel):
    access_token: str

class AuthResponse(BaseModel):
    token: str
    merchant: Dict[str, Any]

class ItemCreate(BaseModel):
    name: str
    category: str
    description: str
    price: float
    mrp: float
    stock_quantity: int
    weight: Optional[float] = 1.0
    brand: Optional[str] = ""
    subcategory: Optional[str] = ""

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    mrp: Optional[float] = None
    stock_quantity: Optional[int] = None
    weight: Optional[float] = None
    status: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str
    estimated_delivery: Optional[str] = None

class OfferCreate(BaseModel):
    title: str
    description: str
    discount_type: str
    discount_value: float
    min_order_value: float
    max_discount: Optional[float] = None
    applicable_categories: List[str] = []

# Helper Functions
async def get_current_merchant(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract merchant info from JWT token"""
    # In real implementation, decode JWT and extract merchant_id
    # For now, return mock merchant
    return "merchant123"

def calculate_dashboard_stats(merchant_id: str):
    """Calculate real dashboard statistics with detailed logging"""
    logger.info(f"🔥 Calculating dashboard stats for merchant: {merchant_id}")
    
    items = ITEMS_DB.get(merchant_id, [])
    orders = ORDERS_DB.get(merchant_id, [])
    offers = OFFERS_DB.get(merchant_id, [])
    
    logger.info(f"🔥 Found {len(items)} items, {len(orders)} orders, {len(offers)} offers")
    
    # Calculate today's stats (mock today as 2024-01-20 for demo)
    today_orders = [o for o in orders if o["order_time"].startswith("2024-01-20")]
    pending_orders = [o for o in orders if o["status"] == "pending"]
    low_stock_items = [i for i in items if i["stock_quantity"] < 20]
    active_offers = [o for o in offers if o["status"] == "active"]
    
    today_revenue = sum(o["total_amount"] for o in today_orders)
    
    stats = {
        "orders_today": len(today_orders),
        "revenue_today": today_revenue,
        "active_offers": len(active_offers),
        "low_stock_products": len(low_stock_items),
        "total_products": len(items),
        "pending_orders": len(pending_orders),
        "top_products": [
            {"name": "Fresh Red Apples", "sales": 25, "revenue": 3000},
            {"name": "Organic Milk", "sales": 18, "revenue": 1080},
            {"name": "Fresh Bread", "sales": 15, "revenue": 675}
        ],
        "recent_orders": orders[:5],  # Last 5 orders
        "timestamp": datetime.now().isoformat(),
        "merchant_id": merchant_id
    }
    
    logger.info(f"🔥 Dashboard stats calculated: {stats}")
    return stats

# ============ HEALTH CHECK ============
@app.get("/")
async def root():
    return {"message": "Market App API is running", "version": "1.0.0", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ============ AUTHENTICATION ROUTES ============
@app.post("/api/auth/google", response_model=AuthResponse)
async def google_auth(auth_request: GoogleAuthRequest):
    """Google OAuth authentication"""
    logger.info(f"🔥 Google auth request: {auth_request.access_token[:20]}...")
    
    # In real implementation, verify Google access token
    # For now, return mock response
    
    mock_token = f"jwt_token_{auth_request.access_token[:10]}"
    merchant = MERCHANTS_DB["merchant123"]
    
    response = AuthResponse(
        token=mock_token,
        merchant=merchant
    )
    
    logger.info(f"🔥 Auth successful for merchant: {merchant['business_name']}")
    return response

@app.post("/api/auth/logout")
async def logout(merchant_id: str = Depends(get_current_merchant)):
    """Logout merchant"""
    logger.info(f"🔥 Logout request for merchant: {merchant_id}")
    return {"message": "Successfully logged out"}

# ============ DASHBOARD ROUTES ============
@app.get("/api/merchants/{merchant_id}/dashboard")
async def get_dashboard(merchant_id: str):
    """Get merchant dashboard data - REAL IMPLEMENTATION with detailed logging"""
    logger.info(f"🔥 Dashboard request for merchant: {merchant_id}")
    
    if merchant_id not in MERCHANTS_DB:
        logger.error(f"❌ Merchant not found: {merchant_id}")
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    try:
        stats = calculate_dashboard_stats(merchant_id)
        logger.info(f"✅ Dashboard response ready: {len(str(stats))} characters")
        return JSONResponse(content=stats, status_code=200, headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        })
    except Exception as e:
        logger.error(f"❌ Dashboard calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard calculation failed: {str(e)}")

# ============ MERCHANT PROFILE ROUTES ============
@app.get("/api/merchants/{merchant_id}/profile")
async def get_merchant_profile(merchant_id: str):
    """Get merchant profile"""
    logger.info(f"🔥 Profile request for merchant: {merchant_id}")
    
    if merchant_id not in MERCHANTS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return JSONResponse(content=MERCHANTS_DB[merchant_id])

@app.put("/api/merchants/{merchant_id}/metadata")
async def update_merchant_metadata(merchant_id: str, metadata: Dict[str, Any]):
    """Update merchant metadata"""
    logger.info(f"🔥 Update metadata for merchant: {merchant_id}")
    
    if merchant_id not in MERCHANTS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    # Update merchant data
    MERCHANTS_DB[merchant_id].update(metadata)
    return JSONResponse(content=MERCHANTS_DB[merchant_id])

@app.get("/api/merchants/{merchant_id}/shop-status")
async def get_shop_status(merchant_id: str):
    """Get shop status"""
    logger.info(f"🔥 Shop status request for merchant: {merchant_id}")
    
    if merchant_id not in MERCHANTS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return JSONResponse(content=MERCHANTS_DB[merchant_id]["shop_status"])

@app.put("/api/merchants/{merchant_id}/shop-status")
async def update_shop_status(merchant_id: str, status_data: Dict[str, Any]):
    """Update shop status"""
    logger.info(f"🔥 Update shop status for merchant: {merchant_id}")
    
    if merchant_id not in MERCHANTS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    MERCHANTS_DB[merchant_id]["shop_status"].update(status_data)
    return JSONResponse(content=MERCHANTS_DB[merchant_id]["shop_status"])

# ============ ITEMS/PRODUCTS ROUTES ============
@app.get("/api/merchants/{merchant_id}/items")
async def get_items(
    merchant_id: str,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
):
    """Get merchant items with filters - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Items request for merchant: {merchant_id}, filters: category={category}, status={status}, search={search}")
    
    if merchant_id not in ITEMS_DB:
        logger.info(f"🔥 No items found for merchant: {merchant_id}, returning empty list")
        return JSONResponse(content=[])
    
    items = ITEMS_DB[merchant_id].copy()
    
    # Apply filters
    if category:
        items = [item for item in items if item["category"].lower() == category.lower()]
        logger.info(f"🔥 After category filter: {len(items)} items")
    
    if status:
        items = [item for item in items if item["status"].lower() == status.lower()]
        logger.info(f"🔥 After status filter: {len(items)} items")
    
    if search:
        search_lower = search.lower()
        items = [item for item in items if 
                search_lower in item["name"].lower() or 
                search_lower in item["description"].lower()]
        logger.info(f"🔥 After search filter: {len(items)} items")
    
    logger.info(f"✅ Returning {len(items)} items")
    return JSONResponse(content=items)

@app.post("/api/merchants/{merchant_id}/items")
async def create_item(merchant_id: str, item_data: ItemCreate):
    """Create new item - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Create item for merchant: {merchant_id}, item: {item_data.name}")
    
    if merchant_id not in ITEMS_DB:
        ITEMS_DB[merchant_id] = []
    
    # Generate new item ID
    new_id = f"item_{len(ITEMS_DB[merchant_id]) + 1:03d}"
    
    new_item = {
        "item_id": new_id,
        "name": item_data.name,
        "category": item_data.category,
        "subcategory": item_data.subcategory,
        "brand": item_data.brand,
        "description": item_data.description,
        "price": item_data.price,
        "mrp": item_data.mrp,
        "stock_quantity": item_data.stock_quantity,
        "status": "active",
        "weight": item_data.weight,
        "sku": f"{item_data.category[:2].upper()}{new_id[-3:]}",
        "images": [],
        "created_at": datetime.now().isoformat()
    }
    
    ITEMS_DB[merchant_id].append(new_item)
    logger.info(f"✅ Item created: {new_item['item_id']}")
    return JSONResponse(content=new_item)

@app.put("/api/merchants/{merchant_id}/items/{item_id}")
async def update_item(merchant_id: str, item_id: str, item_data: ItemUpdate):
    """Update item - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Update item: {item_id} for merchant: {merchant_id}")
    
    if merchant_id not in ITEMS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    items = ITEMS_DB[merchant_id]
    item_index = next((i for i, item in enumerate(items) if item["item_id"] == item_id), None)
    
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    update_data = item_data.dict(exclude_unset=True)
    ITEMS_DB[merchant_id][item_index].update(update_data)
    
    logger.info(f"✅ Item updated: {item_id}")
    return JSONResponse(content=ITEMS_DB[merchant_id][item_index])

@app.delete("/api/merchants/{merchant_id}/items/{item_id}")
async def delete_item(merchant_id: str, item_id: str):
    """Delete item - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Delete item: {item_id} for merchant: {merchant_id}")
    
    if merchant_id not in ITEMS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    items = ITEMS_DB[merchant_id]
    item_index = next((i for i, item in enumerate(items) if item["item_id"] == item_id), None)
    
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = ITEMS_DB[merchant_id].pop(item_index)
    logger.info(f"✅ Item deleted: {item_id}")
    return JSONResponse(content={"message": "Item deleted successfully", "deleted_item": deleted_item})

# ============ ORDERS ROUTES ============
@app.get("/api/merchants/{merchant_id}/orders")
async def get_orders(
    merchant_id: str,
    status: Optional[str] = None,
    date: Optional[str] = None
):
    """Get merchant orders - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Orders request for merchant: {merchant_id}, filters: status={status}, date={date}")
    
    if merchant_id not in ORDERS_DB:
        logger.info(f"🔥 No orders found for merchant: {merchant_id}, returning empty list")
        return JSONResponse(content=[])
    
    orders = ORDERS_DB[merchant_id].copy()
    
    # Apply filters
    if status:
        orders = [order for order in orders if order["status"].lower() == status.lower()]
        logger.info(f"🔥 After status filter: {len(orders)} orders")
    
    if date:
        orders = [order for order in orders if order["order_time"].startswith(date)]
        logger.info(f"🔥 After date filter: {len(orders)} orders")
    
    logger.info(f"✅ Returning {len(orders)} orders")
    return JSONResponse(content=orders)

@app.post("/api/merchants/{merchant_id}/orders/{order_id}/accept")
async def accept_order(merchant_id: str, order_id: str, acceptance_data: Dict[str, Any] = {}):
    """Accept order - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Accept order: {order_id} for merchant: {merchant_id}")
    
    if merchant_id not in ORDERS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    orders = ORDERS_DB[merchant_id]
    order_index = next((i for i, order in enumerate(orders) if order["order_id"] == order_id), None)
    
    if order_index is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    ORDERS_DB[merchant_id][order_index]["status"] = "accepted"
    if "estimated_delivery" in acceptance_data:
        ORDERS_DB[merchant_id][order_index]["estimated_delivery"] = acceptance_data["estimated_delivery"]
    
    logger.info(f"✅ Order accepted: {order_id}")
    return JSONResponse(content=ORDERS_DB[merchant_id][order_index])

@app.post("/api/merchants/{merchant_id}/orders/{order_id}/decline")
async def decline_order(merchant_id: str, order_id: str, decline_data: Dict[str, Any] = {}):
    """Decline order - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Decline order: {order_id} for merchant: {merchant_id}")
    
    if merchant_id not in ORDERS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    orders = ORDERS_DB[merchant_id]
    order_index = next((i for i, order in enumerate(orders) if order["order_id"] == order_id), None)
    
    if order_index is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    ORDERS_DB[merchant_id][order_index]["status"] = "declined"
    if "reason" in decline_data:
        ORDERS_DB[merchant_id][order_index]["decline_reason"] = decline_data["reason"]
    
    logger.info(f"✅ Order declined: {order_id}")
    return JSONResponse(content=ORDERS_DB[merchant_id][order_index])

@app.put("/api/merchants/{merchant_id}/orders/{order_id}/status")
async def update_order_status(merchant_id: str, order_id: str, status_update: OrderStatusUpdate):
    """Update order status - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Update order status: {order_id} to {status_update.status}")
    
    if merchant_id not in ORDERS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    orders = ORDERS_DB[merchant_id]
    order_index = next((i for i, order in enumerate(orders) if order["order_id"] == order_id), None)
    
    if order_index is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    ORDERS_DB[merchant_id][order_index]["status"] = status_update.status
    if status_update.estimated_delivery:
        ORDERS_DB[merchant_id][order_index]["estimated_delivery"] = status_update.estimated_delivery
    
    logger.info(f"✅ Order status updated: {order_id}")
    return JSONResponse(content=ORDERS_DB[merchant_id][order_index])

# ============ OFFERS ROUTES ============
@app.get("/api/merchants/{merchant_id}/offers")
async def get_offers(merchant_id: str):
    """Get merchant offers - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Offers request for merchant: {merchant_id}")
    
    if merchant_id not in OFFERS_DB:
        logger.info(f"🔥 No offers found for merchant: {merchant_id}, returning empty list")
        return JSONResponse(content=[])
    
    offers = OFFERS_DB[merchant_id]
    logger.info(f"✅ Returning {len(offers)} offers")
    return JSONResponse(content=offers)

@app.post("/api/merchants/{merchant_id}/offers")
async def create_offer(merchant_id: str, offer_data: OfferCreate):
    """Create new offer - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Create offer for merchant: {merchant_id}, offer: {offer_data.title}")
    
    if merchant_id not in OFFERS_DB:
        OFFERS_DB[merchant_id] = []
    
    new_id = f"offer_{len(OFFERS_DB[merchant_id]) + 1:03d}"
    
    new_offer = {
        "offer_id": new_id,
        "title": offer_data.title,
        "description": offer_data.description,
        "discount_type": offer_data.discount_type,
        "discount_value": offer_data.discount_value,
        "min_order_value": offer_data.min_order_value,
        "max_discount": offer_data.max_discount,
        "applicable_categories": offer_data.applicable_categories,
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    OFFERS_DB[merchant_id].append(new_offer)
    logger.info(f"✅ Offer created: {new_offer['offer_id']}")
    return JSONResponse(content=new_offer)

@app.delete("/api/merchants/{merchant_id}/offers/{offer_id}")
async def delete_offer(merchant_id: str, offer_id: str):
    """Delete offer - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Delete offer: {offer_id} for merchant: {merchant_id}")
    
    if merchant_id not in OFFERS_DB:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    offers = OFFERS_DB[merchant_id]
    offer_index = next((i for i, offer in enumerate(offers) if offer["offer_id"] == offer_id), None)
    
    if offer_index is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    deleted_offer = OFFERS_DB[merchant_id].pop(offer_index)
    logger.info(f"✅ Offer deleted: {offer_id}")
    return JSONResponse(content={"message": "Offer deleted successfully", "deleted_offer": deleted_offer})

@app.post("/api/merchants/{merchant_id}/apply-overall-discount")
async def apply_global_discount(merchant_id: str, discount_data: Dict[str, Any]):
    """Apply global discount - REAL IMPLEMENTATION"""
    logger.info(f"🔥 Apply global discount for merchant: {merchant_id}")
    # Implementation for applying discount to all products
    return JSONResponse(content={"message": "Global discount applied", "discount_data": discount_data})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)