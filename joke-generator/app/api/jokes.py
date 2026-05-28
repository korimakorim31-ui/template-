"""Joke endpoints"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.joke import Joke
from app.services.joke_service import JokeService
from app.services.external_api import ExternalAPIService

router = APIRouter()

class JokeResponse(BaseModel):
    """Joke response model"""
    id: int
    content: str
    setup: Optional[str] = None
    delivery: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    source: str
    rating: float
    rating_count: int
    view_count: int
    created_at: str
    
    class Config:
        from_attributes = True

class JokeSearchResponse(BaseModel):
    """Search response"""
    total: int
    results: List[JokeResponse]

@router.get("/random", response_model=JokeResponse)
async def get_random_joke(
    type: Optional[str] = Query(None, description="Joke type: general, programming, knock-knock, dad"),
    exclude_words: Optional[str] = Query(None, description="Comma-separated words to exclude"),
    db: Session = Depends(get_db)
):
    """Get a random joke"""
    try:
        joke_service = JokeService(db)
        external_api = ExternalAPIService()
        
        # Try to get from external API first
        try:
            joke_data = await external_api.get_random_joke(
                joke_type=type,
                exclude_words=exclude_words
            )
            
            # Save to database
            joke = joke_service.save_joke(joke_data)
            # Increment view count
            joke.view_count += 1
            db.commit()
            
            return joke
        except Exception as e:
            # Fallback to database
            joke = joke_service.get_random_from_db(joke_type=type)
            if joke:
                joke.view_count += 1
                db.commit()
                return joke
            raise HTTPException(status_code=503, detail="Unable to fetch jokes at the moment")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/random/batch", response_model=List[JokeResponse])
async def get_random_jokes_batch(
    count: int = Query(5, ge=1, le=20, description="Number of jokes to fetch"),
    type: Optional[str] = Query(None, description="Joke type"),
    db: Session = Depends(get_db)
):
    """Get multiple random jokes"""
    try:
        joke_service = JokeService(db)
        jokes = []
        
        for _ in range(count):
            joke = db.query(Joke).order_by(Joke.id).limit(count).all()
            if joke:
                jokes.extend(joke)
        
        return jokes[:count] if jokes else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=JokeSearchResponse)
async def search_jokes(
    keyword: str = Query(..., min_length=1, description="Search keyword"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search jokes by keyword"""
    try:
        joke_service = JokeService(db)
        results = joke_service.search_jokes(keyword, skip, limit)
        total = db.query(Joke).filter(Joke.content.ilike(f"%{keyword}%")).count()
        
        return {
            "total": total,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{joke_id}", response_model=JokeResponse)
async def get_joke(
    joke_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific joke"""
    joke = db.query(Joke).filter(Joke.id == joke_id).first()
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    
    # Increment view count
    joke.view_count += 1
    db.commit()
    
    return joke

@router.post("/", response_model=JokeResponse)
async def create_joke(
    content: str,
    type: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new joke"""
    try:
        joke = Joke(
            content=content,
            type=type,
            category=category,
            source="manual",
        )
        db.add(joke)
        db.commit()
        db.refresh(joke)
        return joke
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{joke_id}")
async def delete_joke(
    joke_id: int,
    db: Session = Depends(get_db)
):
    """Delete a joke"""
    joke = db.query(Joke).filter(Joke.id == joke_id).first()
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    
    db.delete(joke)
    db.commit()
    
    return {"status": "deleted", "id": joke_id}
