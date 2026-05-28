"""Joke rating model"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class JokeRating(Base):
    """User rating for jokes"""
    __tablename__ = "joke_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    joke_id = Column(Integer, ForeignKey("jokes.id"), nullable=False)
    user_id = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<JokeRating joke_id={self.joke_id} rating={self.rating}>"
