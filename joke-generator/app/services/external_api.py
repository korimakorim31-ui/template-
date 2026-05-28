"""External API service for fetching jokes"""

import httpx
import asyncio
from typing import Optional, Dict, Any
from app.config import settings

class ExternalAPIService:
    """Service for external joke APIs"""
    
    JOKEAPI_BASE_URL = "https://jokeapi.dev/api/joke"
    OFFICIAL_JOKES_BASE_URL = "https://official-joke-api.appspot.com"
    
    async def get_random_joke(
        self,
        joke_type: Optional[str] = None,
        exclude_words: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch random joke from external API"""
        try:
            # Try JokeAPI first
            return await self._get_from_jokeapi(joke_type, exclude_words)
        except:
            try:
                # Fallback to Official Jokes API
                return await self._get_from_official_api(joke_type)
            except Exception as e:
                raise Exception(f"Failed to fetch joke: {str(e)}")
    
    async def _get_from_jokeapi(
        self,
        joke_type: Optional[str] = None,
        exclude_words: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch from JokeAPI"""
        # Map internal types to JokeAPI types
        type_mapping = {
            "programming": "Programming",
            "general": "General",
            "knock-knock": "Knock-knock",
            "dad": "General",
        }
        
        api_type = type_mapping.get(joke_type, "Any")
        url = f"{self.JOKEAPI_BASE_URL}/{api_type}"
        
        params = {
            "format": "json",
            "safe-mode": True,
        }
        
        if exclude_words:
            params["blacklistFlags"] = exclude_words
        
        async with httpx.AsyncClient(timeout=settings.JOKE_API_TIMEOUT) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return self._format_jokeapi_response(data)
    
    async def _get_from_official_api(self, joke_type: Optional[str] = None) -> Dict[str, Any]:
        """Fetch from Official Jokes API"""
        type_mapping = {
            "programming": "programming",
            "knock-knock": "knock-knock",
            "general": "general",
        }
        
        api_type = type_mapping.get(joke_type, "random")
        url = f"{self.OFFICIAL_JOKES_BASE_URL}/jokes/{api_type}/random"
        
        async with httpx.AsyncClient(timeout=settings.JOKE_API_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            return self._format_official_api_response(data)
    
    def _format_jokeapi_response(self, data: Dict) -> Dict[str, Any]:
        """Format JokeAPI response"""
        if data.get("type") == "twopart":
            return {
                "content": f"{data['setup']} {data['delivery']}",
                "setup": data["setup"],
                "delivery": data["delivery"],
                "type": "two-part",
                "category": data.get("category", "").lower(),
                "source": "jokeapi",
                "source_id": f"jokeapi_{data.get('id', '')}",
            }
        else:
            return {
                "content": data["joke"],
                "type": "single",
                "category": data.get("category", "").lower(),
                "source": "jokeapi",
                "source_id": f"jokeapi_{data.get('id', '')}",
            }
    
    def _format_official_api_response(self, data: Dict) -> Dict[str, Any]:
        """Format Official Jokes API response"""
        joke_type = data.get("type", "general")
        
        if joke_type == "twopart":
            return {
                "content": f"{data['setup']} {data['delivery']}",
                "setup": data["setup"],
                "delivery": data["delivery"],
                "type": joke_type,
                "source": "official-joke-api",
                "source_id": f"official_{data.get('id', '')}",
            }
        else:
            return {
                "content": data["joke"],
                "type": joke_type,
                "source": "official-joke-api",
                "source_id": f"official_{data.get('id', '')}",
            }
