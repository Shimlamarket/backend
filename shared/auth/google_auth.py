"""
Google OAuth 2.0 authentication service
"""
import os
import jwt
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from shared.models.base import BaseUser, UserRole


class GoogleAuthService:
    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.jwt_secret = os.getenv("JWT_SECRET", "your-secret-key")
        self.jwt_algorithm = "HS256"
        self.jwt_expiry_hours = 24
        
    async def verify_google_token(self, access_token: str) -> Dict:
        """Verify Google access token and get user info"""
        try:
            # Verify token with Google
            response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google access token"
                )
            
            user_info = response.json()
            return user_info
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to verify Google token: {str(e)}"
            )
    
    def create_jwt_token(self, user_data: Dict) -> str:
        """Create JWT token for authenticated user"""
        payload = {
            "user_id": user_data["user_id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "exp": datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token
    
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
        
        # Create JWT token
        jwt_token = self.create_jwt_token(user_data)
        
        return {
            "token": jwt_token,
            "user": user_data
        }


# Global instance
google_auth_service = GoogleAuthService() 