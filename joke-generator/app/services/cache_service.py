"""Caching service"""

import json
from typing import Optional, Any
import redis
from app.config import settings

class CacheService:
    """Service for caching operations"""
    
    def __init__(self):
        if settings.CACHE_ENABLED:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        else:
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except:
            pass
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or settings.JOKE_CACHE_TTL
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
            return True
        except:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except:
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            return True
        except:
            return False
