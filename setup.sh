#!/bin/bash

# Three-App Architecture Setup Script
echo "🏪 Setting up Three-App Architecture..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Docker is installed (optional)
if ! command -v docker &> /dev/null; then
    print_warning "Docker is not installed. You'll need to run DynamoDB manually."
fi

print_status "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp env.example .env
    print_warning "Please edit .env file with your configuration"
else
    print_status ".env file already exists"
fi

# Setup frontend apps
print_status "Setting up frontend applications..."

# Customer App
if [ -d "frontend/customer-app" ]; then
    print_status "Installing Customer App dependencies..."
    cd frontend/customer-app
    npm install
    cd ../..
    print_success "Customer App setup complete"
else
    print_warning "Customer App directory not found"
fi

# Merchant App
if [ -d "frontend/merchant-app" ]; then
    print_status "Installing Merchant App dependencies..."
    cd frontend/merchant-app
    npm install
    cd ../..
    print_success "Merchant App setup complete"
else
    print_warning "Merchant App directory not found"
fi

# Admin App
if [ -d "frontend/admin-app" ]; then
    print_status "Installing Admin App dependencies..."
    cd frontend/admin-app
    npm install
    cd ../..
    print_success "Admin App setup complete"
else
    print_warning "Admin App directory not found"
fi

print_success "Setup completed successfully!"
echo ""
echo "🚀 To start the backend services:"
echo "   python start_all.py"
echo ""
echo "📱 To start the frontend apps:"
echo "   cd frontend/customer-app && npm run dev"
echo "   cd frontend/merchant-app && npm run dev"
echo "   cd frontend/admin-app && npm run dev"
echo ""
echo "🐳 Or use Docker Compose:"
echo "   docker-compose up -d"
echo ""
echo "📚 API Documentation will be available at:"
echo "   http://localhost:8000/docs (API Gateway)"
echo "   http://localhost:8001/docs (Customer API)"
echo "   http://localhost:8002/docs (Merchant API)"
echo "   http://localhost:8003/docs (Admin API)" 