from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for API key authentication.
    
    This middleware checks if the incoming request has a valid API key in the 'x-api-key' header.
    If the API key is invalid or missing, it returns a 403 Forbidden response.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the incoming request and validate the API key.
        
        Args:
            request (Request): The incoming HTTP request
            call_next: The next middleware or route handler in the chain
            
        Returns:
            Response: The response from the next middleware or route handler
            
        Raises:
            HTTPException: If the API key is invalid or missing (status code 403)
        """
        api_key = request.headers.get("x-api-key")
        if api_key != os.getenv("API_KEY"):
            raise HTTPException(status_code=403, detail="Invalid API Key")
        return await call_next(request)


