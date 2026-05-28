"""Joke rating endpoints"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rating import JokeRating
from app.models.favorite import Favorite
from app.services.joke_service import JokeService

router = APIRouter()

class RatingRequest(BaseModel):
    """Rating request model"""
    rating: int  # 1-5 stars

class RatingResponse(BaseModel):
    """Rating response model"""
    id: int
    joke_id: int
    user_id: str
    rating: int
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/{joke_id}/rate", response_model=RatingResponse)
async def rate_joke(
    joke_id: int,
    request: RatingRequest,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Rate a joke"""
    try:
        if not 1 <= request.rating <= 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Check if joke exists
        joke_service = JokeService(db)
        if not joke_service.joke_exists(joke_id):
            raise HTTPException(status_code=404, detail="Joke not found")
        
        # Check if user already rated
        existing_rating = db.query(JokeRating).filter(
            JokeRating.joke_id == joke_id,
            JokeRating.user_id == user_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = request.rating
            db.commit()
            db.refresh(existing_rating)
            return existing_rating
        
        # Create new rating
        rating = JokeRating(
            joke_id=joke_id,
            user_id=user_id,
            rating=request.rating
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        
        # Update joke's average rating
        job_service = JokeService(db)
        job_service.update_joke_rating(joke_id)
        
        return rating
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{joke_id}/ratings", response_model=List[RatingResponse])
async def get_joke_ratings(
    joke_id: int,
    db: Session = Depends(get_db)
):
    """Get all ratings for a joke"""
    ratings = db.query(JokeRating).filter(JokeRating.joke_id == joke_id).all()
    return ratings

@router.post("/{joke_id}/favorite")
async def add_favorite(
    joke_id: int,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Add joke to favorites"""
    try:
        # Check if already favorited
        existing = db.query(Favorite).filter(
            Favorite.joke_id == joke_id,
            Favorite.user_id == user_id
        ).first()
        
        if existing:
            return {"status": "already_favorited", "joke_id": joke_id}
        
        # Add to favorites
        favorite = Favorite(
            joke_id=joke_id,
            user_id=user_id
        )
        db.add(favorite)
        db.commit()
        
        return {"status": "added", "joke_id": joke_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{joke_id}/favorite")
async def remove_favorite(
    joke_id: int,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Remove joke from favorites"""
    try:
        favorite = db.query(Favorite).filter(
            Favorite.joke_id == joke_id,
            Favorite.user_id == user_id
        ).first()
        
        if not favorite:
            raise HTTPException(status_code=404, detail="Favorite not found")
        
        db.delete(favorite)
        db.commit()
        
        return {"status": "removed", "joke_id": joke_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/favorites")
async def get_favorites(
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's favorite jokes"""
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    return {
        "user_id": user_id,
        "count": len(favorites),
        "favorites": [f.joke_id for f in favorites]
    }
