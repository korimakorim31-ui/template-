"""Tweet model"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from app.database import Base

class Tweet(Base):
    """Tweet database model"""
    __tablename__ = "tweets"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    original_content = Column(Text, nullable=True)
    topic = Column(String(255), nullable=False)
    language = Column(String(10), default="en")
    tone = Column(String(50), default="neutral")
    has_hashtags = Column(Boolean, default=False)
    has_cta = Column(Boolean, default=False)
    is_thread = Column(Boolean, default=False)
    thread_id = Column(Integer, nullable=True)  # Reference to parent thread
    tweet_index = Column(Integer, nullable=True)  # Position in thread
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Tweet {self.id}: {self.content[:50]}...>"
