"""Meme caption generation endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.meme import Meme
from app.services.meme_service import MemeService

router = APIRouter()

class MemeCaptionRequest(BaseModel):
    """Request to generate meme caption"""
    image_url: str
    topic: str = "crypto"
    language: str = "en"
    meme_type: str = "general"

class MemeResponse(BaseModel):
    """Meme response model"""
    id: int
    image_url: str
    caption: str
    topic: str
    language: str
    meme_type: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/caption", response_model=MemeResponse)
async def generate_meme_caption(
    request: MemeCaptionRequest,
    db: Session = Depends(get_db)
):
    """Generate a meme caption"""
    try:
        meme_service = MemeService()
        caption = await meme_service.generate_caption(
            image_url=request.image_url,
            topic=request.topic,
            language=request.language,
            meme_type=request.meme_type,
        )
        
        meme = Meme(
            image_url=request.image_url,
            caption=caption,
            topic=request.topic,
            language=request.language,
            meme_type=request.meme_type,
        )
        db.add(meme)
        db.commit()
        db.refresh(meme)
        
        return meme
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{meme_id}", response_model=MemeResponse)
async def get_meme(
    meme_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific meme"""
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme

@router.get("/", response_model=List[MemeResponse])
async def list_memes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all generated memes"""
    memes = db.query(Meme).offset(skip).limit(limit).all()
    return memes

@router.delete("/{meme_id}")
async def delete_meme(
    meme_id: int,
    db: Session = Depends(get_db)
):
    """Delete a meme"""
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    
    db.delete(meme)
    db.commit()
    
    return {"status": "deleted", "id": meme_id}
