"""
API Gateway - Routes requests to appropriate backend services
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="API Gateway",
    description="API Gateway for Three-App Architecture",
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

# Service URLs
SERVICES = {
    "customer": "http://localhost:8001",
    "merchant": "http://localhost:8002", 
    "admin": "http://localhost:8003"
}

# Route patterns
ROUTE_PATTERNS = {
    "customer": [
        "/auth/google",
        "/shops",
        "/products", 
        "/orders",
        "/reviews",
        "/addresses",
        "/profile"
    ],
    "merchant": [
        "/auth/google",
        "/dashboard",
        "/shops",
        "/products",
        "/orders", 
        "/profile"
    ],
    "admin": [
        "/auth/google",
        "/dashboard",
        "/shops",
        "/users",
        "/orders",
        "/reviews",
        "/profile"
    ]
}

def determine_service(path: str) -> str:
    """Determine which service should handle the request based on path"""
    # Check exact matches first
    for service, patterns in ROUTE_PATTERNS.items():
        for pattern in patterns:
            if path.startswith(pattern):
                return service
    
    # Default to customer service for unknown routes
    return "customer"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(request: Request, path: str):
    """Proxy request to appropriate backend service"""
    try:
        # Determine target service
        service = determine_service(f"/{path}")
        target_url = f"{SERVICES[service]}/{path}"
        
        logger.info(f"Routing {request.method} {path} to {service} service")
        
        # Get request body
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
        
        # Get headers
        headers = dict(request.headers)
        # Remove host header to avoid conflicts
        headers.pop("host", None)
        
        # Forward request
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                headers=headers,
                content=body,
                timeout=30.0
            )
        
        # Return response
        return response
        
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        logger.error(f"Gateway error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    """API Gateway root endpoint"""
    return {
        "message": "API Gateway for Three-App Architecture",
        "services": {
            "customer": f"{SERVICES['customer']}/docs",
            "merchant": f"{SERVICES['merchant']}/docs", 
            "admin": f"{SERVICES['admin']}/docs"
        },
        "health": {
            "status": "healthy",
            "gateway": "running"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "gateway": "healthy",
        "services": {}
    }
    
    # Check each service
    async with httpx.AsyncClient() as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health", timeout=5.0)
                health_status["services"][service_name] = "healthy" if response.status_code == 200 else "unhealthy"
            except Exception:
                health_status["services"][service_name] = "unreachable"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 