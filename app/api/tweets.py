"""Tweet generation and management endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tweet import Tweet
from app.services.tweet_service import TweetService

router = APIRouter()

class TweetGenerateRequest(BaseModel):
    """Request to generate a tweet"""
    topic: str
    tone: str = "neutral"
    language: str = "en"
    include_cta: bool = False
    include_hashtags: bool = True
    max_length: int = 280

class TweetRewriteRequest(BaseModel):
    """Request to rewrite a tweet"""
    original_tweet: str
    style: str = "formal"
    language: str = "en"
    tone: str = "neutral"

class TweetThreadRequest(BaseModel):
    """Request to generate a tweet thread"""
    topic: str
    thread_length: int = 5
    language: str = "en"
    tone: str = "neutral"

class TweetHashtagRequest(BaseModel):
    """Request to add hashtags to a tweet"""
    tweet_content: str
    count: int = 5
    language: str = "en"

class TweetResponse(BaseModel):
    """Tweet response model"""
    id: int
    content: str
    topic: str
    language: str
    tone: str
    has_hashtags: bool
    has_cta: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/generate", response_model=TweetResponse)
async def generate_tweet(
    request: TweetGenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate a new tweet"""
    try:
        tweet_service = TweetService()
        content = await tweet_service.generate_tweet(
            topic=request.topic,
            tone=request.tone,
            language=request.language,
            include_cta=request.include_cta,
            include_hashtags=request.include_hashtags,
            max_length=request.max_length,
        )
        
        tweet = Tweet(
            content=content,
            topic=request.topic,
            language=request.language,
            tone=request.tone,
            has_cta=request.include_cta,
            has_hashtags=request.include_hashtags,
        )
        db.add(tweet)
        db.commit()
        db.refresh(tweet)
        
        return tweet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rewrite", response_model=TweetResponse)
async def rewrite_tweet(
    request: TweetRewriteRequest,
    db: Session = Depends(get_db)
):
    """Rewrite an existing tweet"""
    try:
        tweet_service = TweetService()
        content = await tweet_service.rewrite_tweet(
            original_tweet=request.original_tweet,
            style=request.style,
            language=request.language,
            tone=request.tone,
        )
        
        tweet = Tweet(
            content=content,
            original_content=request.original_tweet,
            topic="rewritten",
            language=request.language,
            tone=request.tone,
        )
        db.add(tweet)
        db.commit()
        db.refresh(tweet)
        
        return tweet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-hashtags", response_model=dict)
async def add_hashtags(
    request: TweetHashtagRequest,
    db: Session = Depends(get_db)
):
    """Add hashtags to a tweet"""
    try:
        tweet_service = TweetService()
        result = await tweet_service.add_hashtags(
            tweet_content=request.tweet_content,
            count=request.count,
            language=request.language,
        )
        
        return {
            "original": request.tweet_content,
            "with_hashtags": result,
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/thread", response_model=List[TweetResponse])
async def generate_thread(
    request: TweetThreadRequest,
    db: Session = Depends(get_db)
):
    """Generate a tweet thread"""
    try:
        tweet_service = TweetService()
        threads = await tweet_service.generate_thread(
            topic=request.topic,
            thread_length=request.thread_length,
            language=request.language,
            tone=request.tone,
        )
        
        thread_id = None
        saved_tweets = []
        
        for idx, content in enumerate(threads):
            tweet = Tweet(
                content=content,
                topic=request.topic,
                language=request.language,
                tone=request.tone,
                is_thread=True,
                thread_id=thread_id,
                tweet_index=idx,
            )
            db.add(tweet)
            db.flush()
            
            if idx == 0:
                thread_id = tweet.id
                tweet.thread_id = thread_id
            
            saved_tweets.append(tweet)
        
        db.commit()
        return saved_tweets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tweet_id}", response_model=TweetResponse)
async def get_tweet(
    tweet_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific tweet"""
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet

@router.get("/", response_model=List[TweetResponse])
async def list_tweets(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all tweets"""
    tweets = db.query(Tweet).offset(skip).limit(limit).all()
    return tweets

@router.delete("/{tweet_id}")
async def delete_tweet(
    tweet_id: int,
    db: Session = Depends(get_db)
):
    """Delete a tweet"""
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    db.delete(tweet)
    db.commit()
    
    return {"status": "deleted", "id": tweet_id}
