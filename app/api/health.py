"""Health check endpoints"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Crypto KOL Writer Bot",
    }

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "ready": True,
        "timestamp": datetime.now().isoformat(),
    }
