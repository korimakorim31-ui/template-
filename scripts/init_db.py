#!/usr/bin/env python
"""Initialize database with tables and sample data"""

import sys
sys.path.insert(0, '.')

from app.database import engine, Base
from app.models import Tweet, TweetStyle, Meme, User, Hashtag

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
