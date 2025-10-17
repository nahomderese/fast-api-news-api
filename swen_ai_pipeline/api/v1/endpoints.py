"""
Defines all REST API routes following FastAPI best practices.
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from swen_ai_pipeline.models.data_models import (
    RawNewsInput,
    FinalNewsOutput,
    NewsSummary,
    NewsListResponse,
    IngestionResponse
)
from swen_ai_pipeline.services.ingestion_service import get_ingestion_service, IngestionService
from swen_ai_pipeline.db.database import get_db


# Create API router
router = APIRouter()


@router.post(
    "/ingest",
    response_model=IngestionResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest and enrich a news article",
    description="Triggers the AI enrichment pipeline for a raw news article. "
                "Returns the fully enriched article with AI-generated metadata, "
                "media URLs, and contextual information.",
    tags=["News Ingestion"]
)
async def ingest_news(
    raw_input: RawNewsInput,
    db: AsyncSession = Depends(get_db)
) -> IngestionResponse:
    """
    POST /api/v1/ingest - Ingest and enrich a news article.
    
    This endpoint:
    1. Receives raw news article data
    2. Processes it through the AI enrichment pipeline
    3. Stores the enriched data
    4. Returns the complete enriched article
    
    Args:
        raw_input: Raw news article data (title, body, source_url, etc.)
        
    Returns:
        IngestionResponse containing status and enriched article data
        
    Raises:
        HTTPException 500: If ingestion pipeline fails
    """
    try:
        # Create ingestion service with database session
        service = get_ingestion_service(db)
        
        # Process through ingestion service
        enriched_news = await service.ingest_news(raw_input)
        
        return IngestionResponse(
            status="success",
            message="News article successfully ingested and enriched",
            id=enriched_news.id,
            data=enriched_news
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest news article: {str(e)}"
        )


@router.get(
    "/news/{id}",
    response_model=FinalNewsOutput,
    response_model_exclude_none=True,
    summary="Retrieve a news article by ID",
    description="Returns the complete enriched news article for the given UUID identifier.",
    tags=["News Retrieval"]
)
async def get_news_by_id(
    id: str,
    db: AsyncSession = Depends(get_db)
) -> FinalNewsOutput:
    """
    GET /api/v1/news/{id} - Retrieve a single news article.
    
    Args:
        id: Unique UUID identifier for the article
        
    Returns:
        Complete enriched news article
        
    Raises:
        HTTPException 404: If article not found
    """
    service = get_ingestion_service(db)
    news = await service.get_news_by_id(id)
    
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"News article with ID '{id}' not found"
        )
    
    return news


@router.get(
    "/news",
    response_model=NewsListResponse,
    response_model_exclude_none=True,
    summary="List all news articles",
    description="Returns a paginated list of news article summaries. "
                "Includes essential fields like title, summary, tags, and relevance score.",
    tags=["News Retrieval"]
)
async def list_news(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of articles to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of articles to skip"
    ),
    db: AsyncSession = Depends(get_db)
) -> NewsListResponse:
    """
    GET /api/v1/news - List all news articles with pagination.
    
    Args:
        limit: Maximum number of articles to return (1-100, default 50)
        offset: Number of articles to skip (default 0)
        
    Returns:
        NewsListResponse with total count and list of article summaries
    """
    try:
        service = get_ingestion_service(db)
        
        # Get news articles and count
        news_items = await service.get_all_news(limit=limit, offset=offset)
        total_count = await service.get_news_count()
        
        # Convert to summary format
        summaries = [
            NewsSummary(
                id=news.id,
                title=news.title,
                summary=news.summary,
                tags=news.tags,
                relevance_score=news.relevance_score,
                published_at=news.published_at,
                ingested_at=news.ingested_at,
                featured_image_url=news.media.featured_image_url if news.media else None
            )
            for news in news_items
        ]
        
        return NewsListResponse(
            total=total_count,
            items=summaries
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve news list: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Returns the health status of the API service.",
    tags=["System"]
)
async def health_check():
    """
    GET /api/v1/health - Health check endpoint.
    
    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "service": "SWEN AI-Enriched News Pipeline",
        "version": "1.0.0"
    }


# Additional utility endpoints


@router.get(
    "/stats",
    summary="Get pipeline statistics",
    description="Returns statistics about the news pipeline.",
    tags=["System"]
)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    GET /api/v1/stats - Get pipeline statistics.
    
    Returns:
        Statistics about stored articles
    """
    service = get_ingestion_service(db)
    total_count = await service.get_news_count()
    
    return {
        "total_articles": total_count,
        "status": "operational"
    }

