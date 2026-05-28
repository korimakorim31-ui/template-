"""Statistics endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.joke import Joke
from app.models.rating import JokeRating

router = APIRouter()

@router.get("/jokes")
async def get_joke_stats(db: Session = Depends(get_db)):
    """Get joke statistics"""
    total_jokes = db.query(func.count(Joke.id)).scalar()
    total_ratings = db.query(func.count(JokeRating.id)).scalar()
    avg_rating = db.query(func.avg(Joke.rating)).scalar() or 0
    
    # Group by type
    type_stats = db.query(
        Joke.type,
        func.count(Joke.id)
    ).group_by(Joke.type).all()
    
    # Most viewed
    most_viewed = db.query(Joke).order_by(Joke.view_count.desc()).first()
    
    # Highest rated
    highest_rated = db.query(Joke).order_by(Joke.rating.desc()).first()
    
    return {
        "total_jokes": total_jokes,
        "total_ratings": total_ratings,
        "average_rating": round(avg_rating, 2),
        "by_type": {t: c for t, c in type_stats},
        "most_viewed": most_viewed.content if most_viewed else None,
        "highest_rated": highest_rated.content if highest_rated else None,
    }

@router.get("/usage")
async def get_usage_stats(db: Session = Depends(get_db)):
    """Get API usage statistics"""
    total_views = db.query(func.sum(Joke.view_count)).scalar() or 0
    total_ratings = db.query(func.count(JokeRating.id)).scalar()
    
    return {
        "total_views": total_views,
        "total_ratings": total_ratings,
        "avg_views_per_joke": round(total_views / max(db.query(func.count(Joke.id)).scalar(), 1), 2),
    }
