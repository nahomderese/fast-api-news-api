"""
FastAPI application entry point for the SWEN AI-Enriched News Pipeline.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from swen_ai_pipeline.core.config import settings
from swen_ai_pipeline.api.v1.endpoints import router as api_v1_router


# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    description="AI-Enriched News Pipeline using FastAPI and Google Gemini. "
                "Ingests raw news articles and enriches them with AI-generated "
                "summaries, tags, relevance scores, media URLs, and contextual information.",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.allowed_origins == "*" else settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routers
app.include_router(
    api_v1_router,
    prefix=settings.api_prefix,
    tags=["API v1"]
)


# Root endpoint
@app.get(
    "/",
    summary="Root endpoint",
    description="Returns basic information about the API service.",
    tags=["Root"]
)
async def root():
    """Root endpoint returning API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "api_endpoints": {
            "ingest": f"{settings.api_prefix}/ingest",
            "get_news": f"{settings.api_prefix}/news/{{slug}}",
            "list_news": f"{settings.api_prefix}/news",
            "health": f"{settings.api_prefix}/health",
            "stats": f"{settings.api_prefix}/stats"
        }
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup.
    Initialize connections, load models, etc.
    """
    from swen_ai_pipeline.db.database import database
    import os

    
    print(os.getenv("DATABASE_URL"))
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📝 Environment: {settings.environment}")
    print(f"🤖 AI Service: {'Mock' if settings.use_mock_ai else f'Google {settings.gemini_model}'}")
    
    # Initialize database if URL is configured
    if settings.database_url:
        try:
            print(f"🗄️  Initializing database connection...")
            database.init(settings.database_url)
            
            # Create tables if they don't exist
            await database.create_tables()
            print(f"✅ Database initialized successfully")
        except Exception as e:
            print(f"⚠️  Database initialization failed: {e}")
            print(f"⚠️  Running without database persistence")
    else:
        print(f"⚠️  No database URL configured, skipping database initialization")
    
    print(f"📚 API Documentation: http://{settings.host}:{settings.port}/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown.
    Close connections, cleanup resources, etc.
    """
    from swen_ai_pipeline.db.database import database
    
    print(f"👋 Shutting down {settings.app_name}")
    
    # Close database connections
    if database.engine:
        print(f"🗄️  Closing database connections...")
        await database.close()
        print(f"✅ Database connections closed")


# Main entry point for running the application
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level="info"
    )

