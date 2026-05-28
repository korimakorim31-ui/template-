"""Joke service for database operations"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.models.joke import Joke
from app.models.rating import JokeRating

class JokeService:
    """Service for joke operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_joke(self, joke_data: dict) -> Joke:
        """Save joke to database"""
        # Check if already exists
        existing = self.db.query(Joke).filter(
            Joke.content == joke_data.get("content") or
            Joke.source_id == joke_data.get("source_id")
        ).first()
        
        if existing:
            return existing
        
        joke = Joke(
            content=joke_data.get("content"),
            setup=joke_data.get("setup"),
            delivery=joke_data.get("delivery"),
            type=joke_data.get("type"),
            category=joke_data.get("category"),
            source=joke_data.get("source", "external"),
            source_id=joke_data.get("source_id"),
        )
        self.db.add(joke)
        self.db.commit()
        self.db.refresh(joke)
        return joke
    
    def get_random_from_db(self, joke_type: Optional[str] = None) -> Optional[Joke]:
        """Get random joke from database"""
        query = self.db.query(Joke)
        
        if joke_type:
            query = query.filter(Joke.type == joke_type)
        
        return query.order_by(func.random()).first()
    
    def search_jokes(self, keyword: str, skip: int = 0, limit: int = 10) -> List[Joke]:
        """Search jokes by keyword"""
        return self.db.query(Joke).filter(
            Joke.content.ilike(f"%{keyword}%")
        ).offset(skip).limit(limit).all()
    
    def joke_exists(self, joke_id: int) -> bool:
        """Check if joke exists"""
        return self.db.query(Joke).filter(Joke.id == joke_id).first() is not None
    
    def update_joke_rating(self, joke_id: int) -> None:
        """Update average rating for a joke"""
        joke = self.db.query(Joke).filter(Joke.id == joke_id).first()
        if not joke:
            return
        
        avg_rating = self.db.query(func.avg(JokeRating.rating)).filter(
            JokeRating.joke_id == joke_id
        ).scalar()
        
        rating_count = self.db.query(func.count(JokeRating.id)).filter(
            JokeRating.joke_id == joke_id
        ).scalar()
        
        joke.rating = float(avg_rating) if avg_rating else 0.0
        joke.rating_count = rating_count or 0
        self.db.commit()
