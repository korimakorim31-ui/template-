"""Tweet generation and processing service"""

import asyncio
from typing import List
from app.services.ai_service import AIService
from app.services.hashtag_service import HashtagService

class TweetService:
    """Service for tweet operations"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.hashtag_service = HashtagService()
    
    async def generate_tweet(
        self,
        topic: str,
        tone: str = "neutral",
        language: str = "en",
        include_cta: bool = False,
        include_hashtags: bool = True,
        max_length: int = 280,
    ) -> str:
        """Generate a new tweet"""
        prompt = f"""
        Generate a {tone} tweet about {topic} in {language}.
        The tweet should be under {max_length} characters.
        {'Include a call-to-action (CTA) to encourage engagement.' if include_cta else ''}
        {'Include relevant hashtags.' if include_hashtags else ''}
        Only respond with the tweet content, nothing else.
        """
        
        tweet = await self.ai_service.generate(prompt, language)
        return tweet.strip()
    
    async def rewrite_tweet(
        self,
        original_tweet: str,
        style: str = "formal",
        language: str = "en",
        tone: str = "neutral",
    ) -> str:
        """Rewrite an existing tweet in a different style"""
        prompt = f"""
        Rewrite the following tweet in a {style} {tone} style in {language}:
        
        Original: {original_tweet}
        
        Keep the core message but change the tone and style.
        Keep it under 280 characters.
        Only respond with the rewritten tweet.
        """
        
        rewritten = await self.ai_service.generate(prompt, language)
        return rewritten.strip()
    
    async def add_hashtags(
        self,
        tweet_content: str,
        count: int = 5,
        language: str = "en",
    ) -> str:
        """Add relevant hashtags to a tweet"""
        hashtags = await self.hashtag_service.get_relevant_hashtags(
            tweet_content,
            count,
            language
        )
        
        # Combine tweet with hashtags
        combined = f"{tweet_content} {' '.join(hashtags)}"
        
        # Trim if needed to fit Twitter limit
        if len(combined) > 280:
            combined = tweet_content[:260] + "... " + " ".join(hashtags[:3])
        
        return combined
    
    async def generate_thread(
        self,
        topic: str,
        thread_length: int = 5,
        language: str = "en",
        tone: str = "neutral",
    ) -> List[str]:
        """Generate a coherent tweet thread"""
        prompt = f"""
        Generate a {thread_length}-tweet thread about {topic} in {language} with a {tone} tone.
        
        Each tweet should:
        1. Be under 280 characters
        2. Flow naturally into the next tweet
        3. Build on the previous tweet's message
        4. Be numbered (Tweet 1/X, Tweet 2/X, etc.)
        
        Format each tweet on a new line.
        """
        
        response = await self.ai_service.generate(prompt, language)
        tweets = [tweet.strip() for tweet in response.split('\n') if tweet.strip()]
        
        return tweets[:thread_length]
