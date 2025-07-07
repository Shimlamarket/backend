# Three-App Architecture Project Structure

```
backend/
├── shared/                    # Shared services and utilities
│   ├── auth/                 # Google OAuth & JWT handling
│   ├── database/             # DynamoDB schemas and operations
│   ├── models/               # Shared Pydantic models
│   └── utils/                # Common utilities
├── customer_api/             # Customer app backend
├── merchant_api/             # Merchant app backend  
├── admin_api/                # Admin app backend
├── api_gateway/              # API Gateway for routing
└── requirements.txt          # Shared dependencies

frontend/
├── customer-app/             # React app for customers
├── merchant-app/             # React app for merchants
└── admin-app/                # React app for admins
```

## Apps Overview

### 1. Customer App
- Browse shops and products
- Place orders with Cash on Delivery
- Track order status
- Leave reviews and ratings

### 2. Merchant App  
- Manage shop details and products
- Handle incoming orders
- Update order statuses manually
- View customer feedback

### 3. Admin App
- Approve/reject shops
- Manage users and roles
- Oversee orders and content
- Platform configuration 