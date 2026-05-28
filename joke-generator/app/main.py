"""Main FastAPI application for Joke Generator"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import jokes, ratings, stats, websocket_routes

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
    description="A simple yet powerful API that generates random jokes using external APIs",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jokes.router, prefix="/api/jokes", tags=["Jokes"])
app.include_router(ratings.router, prefix="/api/jokes", tags=["Ratings"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])
if settings.ENABLE_WEBSOCKET:
    app.include_router(websocket_routes.router, tags=["WebSocket"])

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
        "message": "Welcome to Random Joke Generator API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "random_joke": "/api/jokes/random",
            "search": "/api/jokes/search",
            "favorites": "/api/jokes/favorites",
            "stats": "/api/stats/jokes",
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Random Joke Generator API",
        "version": settings.APP_VERSION,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )
