"""Favorite joke model"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Favorite(Base):
    """User's favorite jokes"""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    joke_id = Column(Integer, ForeignKey("jokes.id"), nullable=False)
    user_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<Favorite joke_id={self.joke_id} user_id={self.user_id}>"
