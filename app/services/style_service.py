"""Tweet style analysis service"""

from typing import List, Dict
import json

class StyleService:
    """Service for analyzing tweet styles"""
    
    async def analyze_style(self, sample_tweets: List[str]) -> Dict:
        """Analyze characteristics of tweet style"""
        characteristics = {
            "avg_length": sum(len(t) for t in sample_tweets) / len(sample_tweets),
            "emoji_frequency": self._count_emoji_frequency(sample_tweets),
            "hashtag_usage": self._count_hashtag_frequency(sample_tweets),
            "common_words": self._extract_common_words(sample_tweets),
            "tone": self._detect_tone(sample_tweets),
        }
        return characteristics
    
    def _count_emoji_frequency(self, tweets: List[str]) -> str:
        """Count emoji usage frequency"""
        emoji_count = sum(1 for t in tweets for c in t if ord(c) > 127)
        avg = emoji_count / len(tweets) if tweets else 0
        
        if avg > 2:
            return "high"
        elif avg > 1:
            return "medium"
        else:
            return "low"
    
    def _count_hashtag_frequency(self, tweets: List[str]) -> str:
        """Count hashtag usage frequency"""
        hashtag_count = sum(t.count("#") for t in tweets)
        avg = hashtag_count / len(tweets) if tweets else 0
        
        if avg > 3:
            return "high"
        elif avg > 1:
            return "medium"
        else:
            return "low"
    
    def _extract_common_words(self, tweets: List[str]) -> List[str]:
        """Extract common words from tweets"""
        from collections import Counter
        all_words = []
        for tweet in tweets:
            words = tweet.lower().split()
            all_words.extend([w for w in words if len(w) > 3])
        
        counter = Counter(all_words)
        return [word for word, _ in counter.most_common(10)]
    
    def _detect_tone(self, tweets: List[str]) -> str:
        """Detect overall tone of tweets"""
        # Simplified tone detection
        combined = " ".join(tweets).lower()
        
        bullish_words = ["moon", "bullish", "pump", "surge", "rocket"]
        bearish_words = ["crash", "dump", "bearish", "fud", "shorts"]
        
        bullish_count = sum(1 for word in bullish_words if word in combined)
        bearish_count = sum(1 for word in bearish_words if word in combined)
        
        if bullish_count > bearish_count:
            return "bullish"
        elif bearish_count > bullish_count:
            return "bearish"
        else:
            return "neutral"
