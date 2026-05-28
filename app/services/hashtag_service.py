"""Hashtag service for extracting and suggesting hashtags"""

from typing import List
import re
from app.config import settings

class HashtagService:
    """Service for hashtag operations"""
    
    # Common crypto hashtags
    CRYPTO_HASHTAGS = {
        "bitcoin": ["#Bitcoin", "#BTC", "#hodl", "#Blockchain"],
        "ethereum": ["#Ethereum", "#ETH", "#Web3", "#DeFi"],
        "defi": ["#DeFi", "#YieldFarming", "#LiquidityMining", "#SmartContract"],
        "nft": ["#NFT", "#NFTs", "#Web3", "#Metaverse"],
        "crypto": ["#Crypto", "#CryptoNews", "#CryptoTrading", "#blockchain"],
        "trading": ["#Trading", "#Trader", "#TradingSignals", "#TA"],
        "bullish": ["#Bullish", "#Moon", "#ToTheMoon", "#Longterm"],
        "bearish": ["#Bearish", "#Dump", "#FUD", "#Shorts"],
    }
    
    async def get_relevant_hashtags(
        self,
        content: str,
        count: int = 5,
        language: str = "en",
    ) -> List[str]:
        """Get relevant hashtags for content"""
        hashtags = []
        content_lower = content.lower()
        
        # Match keywords and get corresponding hashtags
        for keyword, tags in self.CRYPTO_HASHTAGS.items():
            if keyword in content_lower:
                hashtags.extend(tags)
        
        # Remove duplicates and limit
        hashtags = list(set(hashtags))[:count]
        
        # If not enough hashtags found, add generic ones
        if len(hashtags) < count:
            generic_tags = ["#Crypto", "#Web3", "#Blockchain", "#CryptoNews"]
            hashtags.extend(generic_tags)
            hashtags = list(set(hashtags))[:count]
        
        return hashtags
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract existing hashtags from text"""
        return re.findall(r"#\w+", text)
