"""Meme caption generation service"""

from app.services.ai_service import AIService

class MemeService:
    """Service for meme caption generation"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_caption(
        self,
        image_url: str,
        topic: str = "crypto",
        language: str = "en",
        meme_type: str = "general",
    ) -> str:
        """Generate a meme caption"""
        prompt = f"""
        Generate a funny and engaging meme caption for a {meme_type} meme about {topic} in {language}.
        
        Guidelines:
        - Make it funny and relatable to crypto community
        - Keep it concise (1-2 lines)
        - Use relevant slang if appropriate
        - Make it shareable on social media
        
        Only respond with the caption.
        """
        
        caption = await self.ai_service.generate(prompt, language, max_tokens=100)
        return caption.strip()
