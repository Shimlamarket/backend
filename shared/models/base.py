"""
Base models for the platform
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    MERCHANT = "merchant"
    ADMIN = "admin"


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ShopStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class DeliveryType(str, Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"


class BaseUser(BaseModel):
    user_id: str = Field(..., description="Unique user ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="User role")
    profile_image: Optional[str] = Field(None, description="Profile image URL")
    phone: Optional[str] = Field(None, description="Phone number")
    is_active: bool = Field(True, description="Account status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Address(BaseModel):
    address_id: str = Field(..., description="Unique address ID")
    user_id: str = Field(..., description="User who owns this address")
    label: str = Field(..., description="Address label (Home, Work, etc.)")
    street_address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    postal_code: str = Field(..., description="Postal code")
    country: str = Field(..., description="Country")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    is_default: bool = Field(False, description="Is default address")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Shop(BaseModel):
    shop_id: str = Field(..., description="Unique shop ID")
    merchant_id: str = Field(..., description="Merchant who owns this shop")
    name: str = Field(..., description="Shop name")
    description: Optional[str] = Field(None, description="Shop description")
    category: str = Field(..., description="Shop category")
    logo_url: Optional[str] = Field(None, description="Shop logo URL")
    banner_url: Optional[str] = Field(None, description="Shop banner URL")
    address: str = Field(..., description="Shop address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    postal_code: str = Field(..., description="Postal code")
    country: str = Field(..., description="Country")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    phone: str = Field(..., description="Shop phone")
    email: Optional[str] = Field(None, description="Shop email")
    website: Optional[str] = Field(None, description="Shop website")
    operating_hours: Dict[str, Dict[str, str]] = Field(..., description="Operating hours by day")
    status: ShopStatus = Field(ShopStatus.PENDING_APPROVAL, description="Shop approval status")
    is_open: bool = Field(True, description="Shop is currently open")
    accepting_orders: bool = Field(True, description="Shop is accepting orders")
    rating: float = Field(0.0, description="Average rating")
    total_reviews: int = Field(0, description="Total number of reviews")
    delivery_radius: float = Field(5.0, description="Delivery radius in km")
    minimum_order: float = Field(0.0, description="Minimum order amount")
    delivery_fee: float = Field(0.0, description="Delivery fee")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProductVariant(BaseModel):
    variant_id: str = Field(..., description="Unique variant ID")
    name: str = Field(..., description="Variant name (e.g., 1kg, Large)")
    sku: str = Field(..., description="Stock keeping unit")
    mrp: float = Field(..., description="Maximum retail price")
    selling_price: float = Field(..., description="Selling price")
    stock_quantity: int = Field(..., description="Available stock")
    is_active: bool = Field(True, description="Variant is available")
    weight: Optional[float] = Field(None, description="Weight in kg")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Dimensions")


class Product(BaseModel):
    product_id: str = Field(..., description="Unique product ID")
    shop_id: str = Field(..., description="Shop that sells this product")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: str = Field(..., description="Product category")
    subcategory: Optional[str] = Field(None, description="Product subcategory")
    brand: Optional[str] = Field(None, description="Product brand")
    images: List[str] = Field(default_factory=list, description="Product image URLs")
    variants: List[ProductVariant] = Field(..., description="Product variants")
    is_active: bool = Field(True, description="Product is available")
    rating: float = Field(0.0, description="Average rating")
    total_reviews: int = Field(0, description="Total number of reviews")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OrderItem(BaseModel):
    item_id: str = Field(..., description="Unique item ID")
    product_id: str = Field(..., description="Product ID")
    variant_id: str = Field(..., description="Product variant ID")
    product_name: str = Field(..., description="Product name")
    variant_name: str = Field(..., description="Variant name")
    quantity: int = Field(..., description="Quantity ordered")
    unit_price: float = Field(..., description="Price per unit")
    total_price: float = Field(..., description="Total price for this item")


class Order(BaseModel):
    order_id: str = Field(..., description="Unique order ID")
    customer_id: str = Field(..., description="Customer who placed the order")
    shop_id: str = Field(..., description="Shop that received the order")
    items: List[OrderItem] = Field(..., description="Order items")
    subtotal: float = Field(..., description="Subtotal before fees")
    delivery_fee: float = Field(0.0, description="Delivery fee")
    total_amount: float = Field(..., description="Total order amount")
    status: OrderStatus = Field(OrderStatus.PENDING, description="Order status")
    delivery_type: DeliveryType = Field(..., description="Delivery or pickup")
    delivery_address: Optional[str] = Field(None, description="Delivery address")
    customer_notes: Optional[str] = Field(None, description="Customer notes")
    merchant_notes: Optional[str] = Field(None, description="Merchant notes")
    estimated_delivery: Optional[datetime] = Field(None, description="Estimated delivery time")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Review(BaseModel):
    review_id: str = Field(..., description="Unique review ID")
    customer_id: str = Field(..., description="Customer who wrote the review")
    shop_id: Optional[str] = Field(None, description="Shop being reviewed")
    product_id: Optional[str] = Field(None, description="Product being reviewed")
    order_id: str = Field(..., description="Order this review is for")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    title: Optional[str] = Field(None, description="Review title")
    comment: Optional[str] = Field(None, description="Review comment")
    images: List[str] = Field(default_factory=list, description="Review image URLs")
    is_verified: bool = Field(False, description="Review is from verified purchase")
    is_approved: bool = Field(True, description="Review is approved by admin")
    created_at: datetime = Field(default_factory=datetime.utcnow) 