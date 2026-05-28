"""Hashtag model"""

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Hashtag(Base):
    """Hashtag database model"""
    __tablename__ = "hashtags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(255), unique=True, nullable=False)
    category = Column(String(100))  # crypto, blockchain, defi, etc.
    usage_count = Column(Integer, default=1)
    relevance_score = Column(Integer, default=0)  # 0-100
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Hashtag #{self.tag}>"
