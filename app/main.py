"""Main FastAPI application for AI Crypto KOL Writer Bot"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import (
    tweets,
    styles,
    memes,
    languages,
    health,
)

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered bot for generating and optimizing crypto content",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_ORIGINS
)

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(tweets.router, prefix="/api/tweets", tags=["Tweets"])
app.include_router(styles.router, prefix="/api/styles", tags=["Styles"])
app.include_router(memes.router, prefix="/api/memes", tags=["Memes"])
app.include_router(languages.router, prefix="/api/languages", tags=["Languages"])

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status": "error"},
    )

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Crypto KOL Writer Bot",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/health",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )
