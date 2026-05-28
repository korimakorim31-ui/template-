"""AI service for content generation"""

import asyncio
from typing import Optional
from app.config import settings

class AIService:
    """Service for AI-powered content generation"""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self._init_provider()
    
    def _init_provider(self):
        """Initialize AI provider"""
        if self.provider == "openai":
            import openai
            self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        elif self.provider == "anthropic":
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = settings.ANTHROPIC_MODEL
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    async def generate(
        self,
        prompt: str,
        language: str = "en",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Generate content using AI"""
        try:
            if self.provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are a crypto content writer. Write in {language}."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content
            
            elif self.provider == "anthropic":
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    system=f"You are a crypto content writer. Write in {language}.",
                )
                return response.content[0].text
        
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
