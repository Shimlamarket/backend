"""
Admin API - FastAPI backend for admin app
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
    title="Admin API",
    description="Backend API for Admin App",
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

# Dependency to get current admin
async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current authenticated admin"""
    try:
        user_data = google_auth_service.verify_jwt_token(credentials.credentials)
        user = await db_service.get_user(user_data["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user["role"] != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied. Admin role required.")
        
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

class ShopApprovalRequest(BaseModel):
    status: ShopStatus
    reason: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserStatusUpdate(BaseModel):
    is_active: bool
    reason: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    admin_notes: Optional[str] = None

class ReviewModerationRequest(BaseModel):
    is_approved: bool
    admin_notes: Optional[str] = None

# Authentication routes
@app.post("/auth/google", response_model=AuthResponse)
async def google_auth(auth_request: GoogleAuthRequest):
    """Authenticate admin with Google OAuth"""
    try:
        auth_result = await google_auth_service.authenticate_user(auth_request.access_token)
        
        # Check if user exists in database
        user = await db_service.get_user(auth_result["user"]["user_id"])
        if not user:
            # Create new user with admin role
            auth_result["user"]["role"] = UserRole.ADMIN
            user_model = BaseUser(**auth_result["user"])
            user = await db_service.create_user(user_model)
        elif user["role"] != UserRole.ADMIN:
            # Update role to admin if needed
            await db_service.update_user(user["user_id"], {"role": UserRole.ADMIN})
            user["role"] = UserRole.ADMIN
        
        return AuthResponse(
            token=auth_result["token"],
            user=user
        )
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Authentication failed")

# Dashboard routes
@app.get("/dashboard")
async def get_dashboard(current_admin: Dict = Depends(get_current_admin)):
    """Get admin dashboard overview"""
    try:
        # Get all users
        all_users = await db_service.get_all_users()
        
        # Get all shops
        all_shops = await db_service.get_all_shops()
        
        # Get all orders
        all_orders = await db_service.get_all_orders()
        
        # Get all reviews
        all_reviews = await db_service.get_all_reviews()
        
        # Calculate statistics
        total_users = len(all_users)
        total_shops = len(all_shops)
        total_orders = len(all_orders)
        total_reviews = len(all_reviews)
        
        pending_shop_approvals = len([s for s in all_shops if s["status"] == ShopStatus.PENDING_APPROVAL])
        pending_orders = len([o for o in all_orders if o["status"] == OrderStatus.PENDING])
        pending_reviews = len([r for r in all_reviews if not r["is_approved"]])
        
        total_revenue = sum(o["total_amount"] for o in all_orders if o["status"] == OrderStatus.DELIVERED)
        
        return {
            "statistics": {
                "total_users": total_users,
                "total_shops": total_shops,
                "total_orders": total_orders,
                "total_reviews": total_reviews,
                "pending_shop_approvals": pending_shop_approvals,
                "pending_orders": pending_orders,
                "pending_reviews": pending_reviews,
                "total_revenue": total_revenue
            },
            "recent_activity": {
                "recent_orders": all_orders[-10:],  # Last 10 orders
                "recent_reviews": all_reviews[-10:],  # Last 10 reviews
                "recent_shops": all_shops[-10:]  # Last 10 shops
            }
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard")

# Shop approval routes
@app.get("/shops/pending")
async def get_pending_shops(current_admin: Dict = Depends(get_current_admin)):
    """Get shops pending approval"""
    try:
        all_shops = await db_service.get_all_shops()
        pending_shops = [s for s in all_shops if s["status"] == ShopStatus.PENDING_APPROVAL]
        return {"shops": pending_shops}
    except Exception as e:
        logger.error(f"Error fetching pending shops: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch pending shops")

@app.put("/shops/{shop_id}/approval")
async def approve_shop(
    shop_id: str,
    approval_data: ShopApprovalRequest,
    current_admin: Dict = Depends(get_current_admin)
):
    """Approve or reject a shop"""
    try:
        shop = await db_service.get_shop(shop_id)
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        # Update shop status
        updates = {
            "status": approval_data.status,
            "updated_at": datetime.utcnow()
        }
        
        if approval_data.reason:
            updates["approval_reason"] = approval_data.reason
        
        updated_shop = await db_service.update_shop_status(shop_id, approval_data.status)
        return updated_shop
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating shop approval: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update shop approval")

@app.get("/shops")
async def get_all_shops(
    status: Optional[ShopStatus] = None,
    current_admin: Dict = Depends(get_current_admin)
):
    """Get all shops with optional status filter"""
    try:
        all_shops = await db_service.get_all_shops()
        
        if status:
            all_shops = [s for s in all_shops if s["status"] == status]
        
        return {"shops": all_shops}
    except Exception as e:
        logger.error(f"Error fetching shops: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch shops")

# User management routes
@app.get("/users")
async def get_all_users(current_admin: Dict = Depends(get_current_admin)):
    """Get all users"""
    try:
        all_users = await db_service.get_all_users()
        return {"users": all_users}
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@app.get("/users/{user_id}")
async def get_user(user_id: str, current_admin: Dict = Depends(get_current_admin)):
    """Get specific user details"""
    try:
        user = await db_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")

@app.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_data: UserRoleUpdate,
    current_admin: Dict = Depends(get_current_admin)
):
    """Update user role"""
    try:
        user = await db_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        updated_user = await db_service.update_user(user_id, {"role": role_data.role})
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user role: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user role")

@app.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    status_data: UserStatusUpdate,
    current_admin: Dict = Depends(get_current_admin)
):
    """Update user active status"""
    try:
        user = await db_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        updates = {
            "is_active": status_data.is_active,
            "updated_at": datetime.utcnow()
        }
        
        if status_data.reason:
            updates["status_reason"] = status_data.reason
        
        updated_user = await db_service.update_user(user_id, updates)
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user status")

# Order management routes
@app.get("/orders")
async def get_all_orders(
    status: Optional[OrderStatus] = None,
    current_admin: Dict = Depends(get_current_admin)
):
    """Get all orders with optional status filter"""
    try:
        all_orders = await db_service.get_all_orders()
        
        if status:
            all_orders = [o for o in all_orders if o["status"] == status]
        
        return {"orders": all_orders}
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

@app.get("/orders/{order_id}")
async def get_order(order_id: str, current_admin: Dict = Depends(get_current_admin)):
    """Get specific order details"""
    try:
        order = await db_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")

@app.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    current_admin: Dict = Depends(get_current_admin)
):
    """Update order status (admin override)"""
    try:
        order = await db_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Update order status
        updates = {
            "status": status_data.status,
            "updated_at": datetime.utcnow()
        }
        
        if status_data.admin_notes:
            updates["admin_notes"] = status_data.admin_notes
        
        updated_order = await db_service.update_order_status(order_id, status_data.status)
        return updated_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update order status")

# Review moderation routes
@app.get("/reviews")
async def get_all_reviews(
    is_approved: Optional[bool] = None,
    current_admin: Dict = Depends(get_current_admin)
):
    """Get all reviews with optional approval filter"""
    try:
        all_reviews = await db_service.get_all_reviews()
        
        if is_approved is not None:
            all_reviews = [r for r in all_reviews if r["is_approved"] == is_approved]
        
        return {"reviews": all_reviews}
    except Exception as e:
        logger.error(f"Error fetching reviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch reviews")

@app.get("/reviews/{review_id}")
async def get_review(review_id: str, current_admin: Dict = Depends(get_current_admin)):
    """Get specific review details"""
    try:
        review = await db_service.get_review(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return review
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching review: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch review")

@app.put("/reviews/{review_id}/moderation")
async def moderate_review(
    review_id: str,
    moderation_data: ReviewModerationRequest,
    current_admin: Dict = Depends(get_current_admin)
):
    """Moderate a review (approve/reject)"""
    try:
        review = await db_service.get_review(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        # This would need to be implemented in the database service
        # For now, return the review with updated moderation status
        review["is_approved"] = moderation_data.is_approved
        review["admin_notes"] = moderation_data.admin_notes
        review["moderated_at"] = datetime.utcnow()
        review["moderated_by"] = current_admin["user_id"]
        
        return review
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error moderating review: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to moderate review")

# Profile routes
@app.get("/profile")
async def get_profile(current_admin: Dict = Depends(get_current_admin)):
    """Get admin profile"""
    return current_admin

@app.put("/profile")
async def update_profile(
    updates: Dict[str, Any],
    current_admin: Dict = Depends(get_current_admin)
):
    """Update admin profile"""
    try:
        updated_user = await db_service.update_user(current_admin["user_id"], updates)
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
    uvicorn.run(app, host="0.0.0.0", port=8003) 