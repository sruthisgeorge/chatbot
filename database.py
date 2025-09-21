import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import Config

# Database configuration - supports both SQLite (dev) and PostgreSQL (prod)
def get_database_url():
    """Get database URL from environment or config"""
    # Check for Railway PostgreSQL URL first
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    # Check config
    if Config.DATABASE_URL and Config.DATABASE_URL != "sqlite:///./chatbot.db":
        return Config.DATABASE_URL
    
    # Default to SQLite for development
    return "sqlite:///./chatbot.db"

SQLALCHEMY_DATABASE_URL = get_database_url()

# Create engine with appropriate settings
if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration for production
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
else:
    # SQLite configuration for development
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
