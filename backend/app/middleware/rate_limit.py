"""
Rate Limiting Middleware
"""
from datetime import datetime, timedelta
from typing import Dict, Tuple
from collections import defaultdict
import asyncio
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent abuse
    
    Configuration:
    - Default: 100 requests per minute
    - Auth endpoints: 5 requests per minute
    - Query endpoints: 20 requests per minute
    """
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.storage: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
        
        # Cleanup old entries every 5 minutes
        asyncio.create_task(self._cleanup_task())
    
    async def _cleanup_task(self):
        """Periodically clean up old rate limit entries"""
        while True:
            await asyncio.sleep(300)  # 5 minutes
            await self._cleanup()
    
    async def _cleanup(self):
        """Remove expired rate limit entries"""
        now = datetime.now()
        async with self.lock:
            keys_to_delete = []
            for key, timestamps in self.storage.items():
                # Remove timestamps older than period
                self.storage[key] = [
                    ts for ts in timestamps
                    if (now - ts).total_seconds() < self.period
                ]
                if not self.storage[key]:
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del self.storage[key]
    
    def _get_rate_limit_for_path(self, path: str) -> Tuple[int, int]:
        """
        Get rate limit configuration for path
        
        Args:
            path: Request path
            
        Returns:
            Tuple of (calls, period)
        """
        # Stricter limits for auth endpoints
        if '/auth/' in path:
            return 5, 60  # 5 requests per minute
        
        # Moderate limits for query endpoints
        if '/query/' in path or '/emails/sync' in path:
            return 20, 60  # 20 requests per minute
        
        # Default limits
        return self.calls, self.period
    
    async def dispatch(self, request: Request, call_next):
        """Check rate limit and process request"""
        
        # Get client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"
        
        # Get rate limit for this path
        calls, period = self._get_rate_limit_for_path(request.url.path)
        
        # Check rate limit
        async with self.lock:
            now = datetime.now()
            
            # Remove old timestamps
            self.storage[ip] = [
                ts for ts in self.storage[ip]
                if (now - ts).total_seconds() < period
            ]
            
            # Check if limit exceeded
            if len(self.storage[ip]) >= calls:
                logger.warning(f"Rate limit exceeded for IP: {ip}")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {calls} requests per {period} seconds.",
                    headers={"Retry-After": str(period)}
                )
            
            # Add current timestamp
            self.storage[ip].append(now)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = calls - len(self.storage[ip])
        response.headers["X-RateLimit-Limit"] = str(calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int((now + timedelta(seconds=period)).timestamp()))
        
        return response

