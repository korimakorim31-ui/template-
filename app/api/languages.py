"""Language support endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.language_service import LanguageService

router = APIRouter()

class TranslateRequest(BaseModel):
    """Request to translate content"""
    content: str
    source_language: str = "en"
    target_language: str = "es"

class LanguageResponse(BaseModel):
    """Language response model"""
    code: str
    name: str
    native_name: str

@router.get("/", response_model=List[LanguageResponse])
async def list_languages():
    """List supported languages"""
    language_service = LanguageService()
    return language_service.get_supported_languages()

@router.post("/translate", response_model=dict)
async def translate_content(
    request: TranslateRequest,
):
    """Translate content to another language"""
    try:
        language_service = LanguageService()
        translated = await language_service.translate(
            content=request.content,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        
        return {
            "original": request.content,
            "translated": translated,
            "source_language": request.source_language,
            "target_language": request.target_language,
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect", response_model=dict)
async def detect_language(
    text: str,
):
    """Detect language of text"""
    try:
        language_service = LanguageService()
        language = language_service.detect_language(text)
        
        return {
            "text": text,
            "detected_language": language,
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
