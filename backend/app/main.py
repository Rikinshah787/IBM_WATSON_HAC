"""
OrchestrateIQ - Main FastAPI Application
Provides REST API for AI agent orchestration across business sectors
"""

import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings

from app.orchestrate.agent import OrchestrateAgent
from app.api.routes import router
from app.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings"""
    debug: bool = True
    log_level: str = "INFO"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Global agent instance
agent_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global agent_instance
    
    logger.info("🚀 Starting OrchestrateIQ Backend...")
    logger.info(f"📊 Debug Mode: {settings.debug}")
    logger.info(f"📝 Log Level: {settings.log_level}")
    
    try:
        # Initialize watsonx Orchestrate agent
        logger.info("🔌 Initializing watsonx Orchestrate agent...")
        agent_instance = OrchestrateAgent()
        await agent_instance.initialize()
        logger.info("✅ watsonx Orchestrate agent initialized successfully")
        
        # Store agent in app state
        app.state.agent = agent_instance
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("🛑 Shutting down OrchestrateIQ Backend...")


# Create FastAPI app
app = FastAPI(
    title="OrchestrateIQ API",
    description="AI-Powered Business Command Center with watsonx Orchestrate",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.debug
)

# Configure CORS
origins = settings.cors_origins.split(",") if settings.cors_origins else ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    logger.debug("Root endpoint accessed")
    return {
        "message": "OrchestrateIQ API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint accessed")
    try:
        # Check agent status
        if agent_instance and agent_instance.is_initialized:
            return {
                "status": "healthy",
                "agent": "initialized",
                "timestamp": logging.Formatter().formatTime(logging.LogRecord(
                    name="", level=0, pathname="", lineno=0, msg="", args=(), exc_info=None
                ))
            }
        else:
            return {
                "status": "degraded",
                "agent": "not_initialized"
            }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on port {settings.backend_port}")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

