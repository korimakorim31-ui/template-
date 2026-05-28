"""Joke model"""

from sqlalchemy import Column, String, Text, DateTime, Float, Integer
from sqlalchemy.sql import func
from app.database import Base

class Joke(Base):
    """Joke database model"""
    __tablename__ = "jokes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False, unique=True)
    setup = Column(Text, nullable=True)  # For two-part jokes
    delivery = Column(Text, nullable=True)  # For two-part jokes
    type = Column(String(50), nullable=True)  # general, programming, knock-knock, dad, etc.
    category = Column(String(50), nullable=True)  # science, sports, technology, etc.
    source = Column(String(100), nullable=False)  # jokeapi, official-joke-api, etc.
    source_id = Column(String(255), nullable=True)  # ID from external source
    rating = Column(Float, default=0.0)  # Average rating
    rating_count = Column(Integer, default=0)  # Number of ratings
    view_count = Column(Integer, default=0)  # Number of views
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Joke {self.id}: {self.content[:50]}...>"
