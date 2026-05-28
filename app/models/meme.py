"""Meme model"""

from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.sql import func
from app.database import Base

class Meme(Base):
    """Generated meme caption model"""
    __tablename__ = "memes"
    
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    caption = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    meme_type = Column(String(100))
    topic = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Meme {self.id}: {self.caption[:50]}...>"
