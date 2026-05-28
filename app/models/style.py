"""Tweet style model for learning"""

from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.sql import func
from app.database import Base

class TweetStyle(Base):
    """Tweet style for learning patterns"""
    __tablename__ = "tweet_styles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    sample_tweets = Column(Text)  # JSON array of example tweets
    characteristics = Column(Text)  # JSON object with style characteristics
    language = Column(String(10), default="en")
    word_count_avg = Column(Integer)
    emoji_usage = Column(String(255))
    hashtag_density = Column(String(50))  # low, medium, high
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<TweetStyle {self.name}>"
