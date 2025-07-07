# 🏪 Three-App Architecture - Shop Management Platform

A comprehensive shop management platform with three separate applications: Customer App, Merchant App, and Admin App.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Customer App  │    │  Merchant App   │    │   Admin App     │
│   (React/Vite)  │    │   (React/Vite)  │    │  (React/Vite)   │
│   Port: 3000    │    │   Port: 3001    │    │   Port: 3002    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API Gateway   │
                    │   (FastAPI)     │
                    │   Port: 8000    │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Customer API    │    │ Merchant API    │    │   Admin API     │
│ (FastAPI)       │    │ (FastAPI)       │    │ (FastAPI)       │
│ Port: 8001      │    │ Port: 8002      │    │ Port: 8003      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Shared        │
                    │   Services      │
                    │   (Auth/DB)     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   DynamoDB      │
                    │   (Database)    │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (for DynamoDB local)

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start DynamoDB local:**
   ```bash
   docker run -p 8000:8000 amazon/dynamodb-local
   ```

4. **Start the backend services:**
   ```bash
   # Terminal 1: API Gateway
   python api_gateway/main.py
   
   # Terminal 2: Customer API
   python customer_api/main.py
   
   # Terminal 3: Merchant API
   python merchant_api/main.py
   
   # Terminal 4: Admin API
   python admin_api/main.py
   ```

### Frontend Setup

1. **Install dependencies for each app:**
   ```bash
   # Customer App
   cd frontend/customer-app
   npm install
   
   # Merchant App
   cd ../merchant-app
   npm install
   
   # Admin App
   cd ../admin-app
   npm install
   ```

2. **Start the frontend apps:**
   ```bash
   # Terminal 5: Customer App
   cd frontend/customer-app
   npm run dev
   
   # Terminal 6: Merchant App
   cd ../merchant-app
   npm run dev
   
   # Terminal 7: Admin App
   cd ../admin-app
   npm run dev
   ```

## 📱 Applications

### 🛒 Customer App (Port 3000)

**Features:**
- Browse shops and products
- Search and filter functionality
- Shopping cart management
- Place orders with Cash on Delivery
- Track order status
- Leave reviews and ratings
- Manage profile and addresses

**Tech Stack:**
- React 18 + TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- React Router for navigation
- Zustand for state management
- React Query for data fetching
- Heroicons for icons

### 🏪 Merchant App (Port 3001)

**Features:**
- Google OAuth authentication
- Manage multiple shops
- Create and manage products
- Handle incoming orders
- Update order statuses manually
- View customer feedback
- Dashboard with analytics

**Tech Stack:**
- React 18 + TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- React Router for navigation
- Zustand for state management
- React Query for data fetching

### 👑 Admin App (Port 3002)

**Features:**
- Admin authentication with elevated privileges
- Dashboard with platform overview
- Shop approval queue
- User management and role assignment
- Order oversight and management
- Content moderation (reviews, descriptions)
- Platform configuration

**Tech Stack:**
- React 18 + TypeScript
- Vite for build tooling
- Tailwind CSS + shadcn/ui components
- React Router for navigation
- Zustand for state management
- React Query for data fetching

## 🔧 Backend Services

### API Gateway (Port 8000)

Routes requests to appropriate backend services based on URL patterns.

### Customer API (Port 8001)

Handles customer-specific operations:
- Authentication
- Shop browsing
- Product discovery
- Order placement
- Review management

### Merchant API (Port 8002)

Handles merchant-specific operations:
- Shop management
- Product management
- Order processing
- Analytics

### Admin API (Port 8003)

Handles admin-specific operations:
- User management
- Shop approval
- Content moderation
- Platform oversight

### Shared Services

**Authentication Service:**
- Google OAuth 2.0 integration
- JWT token management
- Role-based access control

**Database Service:**
- DynamoDB integration
- Data models and schemas
- CRUD operations

## 🗄️ Database Schema

### Tables

1. **users** - User accounts and profiles
2. **shops** - Shop information and settings
3. **products** - Product catalog
4. **orders** - Order management
5. **reviews** - Customer reviews and ratings
6. **addresses** - User delivery addresses

### Key Relationships

- Users can have multiple shops (merchants)
- Shops have multiple products
- Orders belong to customers and shops
- Reviews are linked to orders, shops, and products

## 🔐 Authentication & Authorization

### Google OAuth 2.0

All apps use Google OAuth 2.0 for authentication:
1. User authenticates with Google
2. Backend verifies token and creates/updates user
3. JWT token issued for subsequent requests

### Role-Based Access Control

- **Customer**: Browse, order, review
- **Merchant**: Manage shops, products, orders
- **Admin**: Full platform access and moderation

## 🚀 Deployment

### Backend Deployment

```bash
# Build Docker images
docker build -t customer-api ./customer_api
docker build -t merchant-api ./merchant_api
docker build -t admin-api ./admin_api
docker build -t api-gateway ./api_gateway

# Deploy to AWS/GCP/Azure
```

### Frontend Deployment

```bash
# Build for production
cd frontend/customer-app && npm run build
cd ../merchant-app && npm run build
cd ../admin-app && npm run build

# Deploy to Vercel/Netlify
```

## 🧪 Testing

### Backend Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

### Frontend Testing

```bash
# Customer App
cd frontend/customer-app
npm test

# Merchant App
cd ../merchant-app
npm test

# Admin App
cd ../admin-app
npm test
```

## 📊 API Documentation

Each API service provides interactive documentation:

- **API Gateway**: http://localhost:8000/docs
- **Customer API**: http://localhost:8001/docs
- **Merchant API**: http://localhost:8002/docs
- **Admin API**: http://localhost:8003/docs

## 🔧 Configuration

### Environment Variables

```bash
# Database
DYNAMODB_ENDPOINT_URL=http://localhost:8000
AWS_ACCESS_KEY_ID=dummy
AWS_SECRET_ACCESS_KEY=dummy

# Authentication
GOOGLE_CLIENT_ID=your_google_client_id
JWT_SECRET=your_jwt_secret

# Environment
ENVIRONMENT=development
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the code examples

---

**Built with ❤️ using FastAPI, React, and Tailwind CSS**