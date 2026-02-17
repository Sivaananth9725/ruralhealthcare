"""
FastAPI main application for Rural Healthcare Decision Support Bot.
Includes CORS configuration, startup tasks, and route integration.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import engine, Base
from models import PatientQuery
from rag import load_guidelines
from services.llm_service import initialize_groq
from routes.diagnosis import router as diagnosis_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Rural Healthcare Decision Support Bot",
    description="AI-powered healthcare guidance system for rural areas using RAG and Groq LLM",
    version="1.0.0",
)

# Add CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    - Create database tables
    - Load RAG guidelines
    - Initialize Groq LLM service
    """
    logger.info("Application startup initiated...")
    
    try:
        # Create database tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully")
        
    except Exception as e:
        logger.error(f"✗ Error creating database tables: {e}")
    
    try:
        # Load RAG guidelines
        logger.info("Loading medical guidelines for RAG...")
        if load_guidelines():
            logger.info("✓ Medical guidelines loaded successfully")
        else:
            logger.warning("⚠ Medical guidelines not loaded (check guidelines folder)")
        
    except Exception as e:
        logger.error(f"✗ Error loading guidelines: {e}")
    
    try:
        # Initialize Groq LLM
        logger.info("Initializing Groq LLM service...")
        if initialize_groq():
            logger.info("✓ Groq LLM service initialized successfully")
        else:
            logger.warning("⚠ Groq LLM service not initialized (check GROQ_API_KEY)")
        
    except Exception as e:
        logger.error(f"✗ Error initializing Groq LLM: {e}")
    
    logger.info("Application startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Application shutting down...")


# Include routers
app.include_router(diagnosis_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Rural Healthcare Decision Support Bot API",
        "version": "1.0.0",
        "endpoints": {
            "diagnose": "/api/diagnose (POST)",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
