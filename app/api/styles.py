"""Tweet style learning endpoints"""

from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.style import TweetStyle
from app.services.style_service import StyleService

router = APIRouter()

class StyleUploadRequest(BaseModel):
    """Request to upload tweet styles"""
    name: str
    description: str
    sample_tweets: List[str]
    language: str = "en"

class StyleResponse(BaseModel):
    """Style response model"""
    id: int
    name: str
    description: str
    language: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/upload", response_model=StyleResponse)
async def upload_style(
    request: StyleUploadRequest,
    db: Session = Depends(get_db)
):
    """Upload and analyze tweet styles"""
    try:
        style_service = StyleService()
        characteristics = await style_service.analyze_style(
            sample_tweets=request.sample_tweets
        )
        
        style = TweetStyle(
            name=request.name,
            description=request.description,
            sample_tweets=json.dumps(request.sample_tweets),
            characteristics=json.dumps(characteristics),
            language=request.language,
        )
        db.add(style)
        db.commit()
        db.refresh(style)
        
        return style
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[StyleResponse])
async def list_styles(
    language: str = "en",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List learned tweet styles"""
    styles = db.query(TweetStyle).filter(
        TweetStyle.language == language
    ).offset(skip).limit(limit).all()
    return styles

@router.get("/{style_id}", response_model=StyleResponse)
async def get_style(
    style_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific style"""
    style = db.query(TweetStyle).filter(TweetStyle.id == style_id).first()
    if not style:
        raise HTTPException(status_code=404, detail="Style not found")
    return style

@router.delete("/{style_id}")
async def delete_style(
    style_id: int,
    db: Session = Depends(get_db)
):
    """Delete a style"""
    style = db.query(TweetStyle).filter(TweetStyle.id == style_id).first()
    if not style:
        raise HTTPException(status_code=404, detail="Style not found")
    
    db.delete(style)
    db.commit()
    
    return {"status": "deleted", "id": style_id}
