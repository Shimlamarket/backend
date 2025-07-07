"""
Google OAuth 2.0 authentication service
"""
import os
import jwt  # Ensure this is the PyJWT library (install with `pip install PyJWT`)
import requests
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from shared.models.base import BaseUser, UserRole

# Check for shadowing issues
if jwt.__name__ != "jwt":
    raise ImportError("The 'jwt' module is not the correct PyJWT library. Ensure PyJWT is installed and no local 'jwt.py' file exists.")

logger = logging.getLogger(__name__)

# Add CORS middleware to handle OPTIONS requests
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoogleAuthService:
    def __init__(self):
        self.google_client_id = os.getenv("VITE_GOOGLE_CLIENT_ID", "687991270323-2mt9l61alcrjp4nna7gr3ad7av89cpei.apps.googleusercontent.com")
        self.google_client_secret = "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"  # Add client secret validation
        self.jwt_secret = os.getenv("JWT_SECRET", "your-secret-key")
        self.jwt_algorithm = "HS256"
        self.jwt_expiry_hours = 24

        # Log and validate credentials
        if not self.google_client_id:
            logger.info("Missing GOOGLE_CLIENT_ID environment variable.")
            raise RuntimeError("GOOGLE_CLIENT_ID is not set. Please configure it in the environment.")
        if not self.google_client_secret:
            logger.info("Missing GOOGLE_CLIENT_SECRET environment variable.")
            raise RuntimeError("GOOGLE_CLIENT_SECRET is not set. Please configure it in the environment.")
        if not self.jwt_secret:
            logger.info("Missing JWT_SECRET environment variable.")
            raise RuntimeError("JWT_SECRET is not set. Please configure it in the environment.")
        logger.info("GoogleAuthService initialized with valid credentials.")
        
    async def verify_google_token(self, access_token: str) -> Dict:
        """Verify Google access token and get user info"""
        logger.info("Starting verification of Google access token...")
        try:
            if not access_token:
                logger.error("Access token is missing.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Access token is required."
                )
            
            logger.debug(f"Access token received: {access_token}")
            response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            logger.info(f"Google API response status: {response.status_code}")
            logger.debug(f"Google API response headers: {response.headers}")
            logger.debug(f"Google API response body: {response.text}")
            
            if response.status_code != 200:
                logger.error(f"Google token verification failed with status code {response.status_code} and response: {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google access token"
                )
            
            user_info = response.json()
            logger.info("Google token verified successfully.")
            logger.debug(f"User info retrieved: {user_info}")
            return user_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred while verifying Google token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to connect to Google API. Please try again later."
            )
        except Exception as e:
            logger.error(f"Unexpected exception occurred while verifying Google token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to verify Google token: {str(e)}"
            )
    
    def create_jwt_token(self, user_data: Dict) -> str:
        """Create JWT token for authenticated user"""
        try:
            payload = {
                "user_id": user_data["user_id"],
                "email": user_data["email"],
                "role": user_data["role"],
                "exp": datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours),
                "iat": datetime.utcnow()
            }
            
            logger.info(f"Creating JWT token with payload: {payload}")
            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            logger.info(f"JWT token successfully created: {token}")
            return token
        except AttributeError as e:
            logger.info("The 'jwt' module does not have the 'encode' method. Ensure PyJWT is installed.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT library error: 'encode' method not found. Ensure PyJWT is installed."
            )
        except Exception as e:
            logger.info("Error occurred while creating JWT token")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create JWT token: {str(e)}"
            )
    
    def verify_jwt_token(self, token: str) -> Dict:
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def authenticate_user(self, access_token: str) -> Dict:
        """Authenticate user with Google token and return user data with JWT"""
        logger.info("Starting user authentication...")
        logger.info(f"Received access token: {access_token}")
        # Verify Google token
        google_user_info = await self.verify_google_token(access_token)
        
        # Create or get user from database (simplified for demo)
        user_data = {
            "user_id": google_user_info["id"],
            "email": google_user_info["email"],
            "name": google_user_info["name"],
            "profile_image": google_user_info.get("picture"),
            "role": UserRole.CUSTOMER,  # Default role, can be updated by admin
            "is_active": True
        }
        logger.info(f"User data constructed: {user_data}")
        
        # Create JWT token
        jwt_token = self.create_jwt_token(user_data)
        logger.info(f"JWT token created: {jwt_token}")
        
        return {
            "token": jwt_token,
            "user": user_data
        }

# Add a route to handle OPTIONS requests explicitly if needed
@app.options("/auth/google")
async def handle_options():
    logger.info("Handling OPTIONS request for /auth/google")
    return JSONResponse(status_code=status.HTTP_200_OK)

# Global instance
google_auth_service = GoogleAuthService()