from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("x-api-key")
        if api_key != os.getenv("API_KEY"):
            raise HTTPException(status_code=403, detail="Invalid API Key")
        return await call_next(request)

