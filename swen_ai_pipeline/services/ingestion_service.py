"""
Orchestrates the complete news ingestion and enrichment workflow.
"""
from datetime import datetime, timezone
from typing import Optional

from swen_ai_pipeline.models.data_models import (
    RawNewsInput,
    FinalNewsOutput,
    EnrichedNewsMedia,
    EnrichedNewsContext
)
from sqlalchemy.ext.asyncio import AsyncSession

from swen_ai_pipeline.services.ai_service import ai_service
from swen_ai_pipeline.db.repository import get_repository


class IngestionService:
    """
    Service that orchestrates the news ingestion pipeline.
    Coordinates between AI service and repository layer following Clean Architecture.
    """
    
    def __init__(self, db_session: AsyncSession):
        """
        Initialize the ingestion service.
        
        Args:
            db_session: Database session for repository operations
        """
        self.ai_service = ai_service
        self.repository = get_repository(db_session)
    
    async def ingest_news(self, raw_input: RawNewsInput) -> FinalNewsOutput:
        """
        Process and enrich a raw news article through the AI pipeline.
        
        This is the main orchestration method that:
        1. Receives raw news input
        2. Enriches it using AI services
        3. Stores the enriched data
        4. Returns the complete enriched output
        
        Args:
            raw_input: Raw news article data
            
        Returns:
            Fully enriched news output
            
        Raises:
            Exception: If any step in the pipeline fails
        """
        try:
            # Step 1: AI Enrichment
            enriched_data = await self.ai_service.enrich_news(raw_input)
            
            # Step 2: Construct the final output model
            final_output = FinalNewsOutput(
                # Original fields
                title=raw_input.title,
                body=raw_input.body,
                source_url=str(raw_input.source_url),
                publisher=raw_input.author,  # Map author to publisher
                published_at=raw_input.published_date,  # Map published_date to published_at
                
                # AI-generated core fields
                summary=enriched_data["summary"],
                tags=enriched_data["tags"],
                relevance_score=enriched_data["relevance_score"],
                
                # Nested enriched objects
                media=enriched_data["media"],
                context=enriched_data["context"],
                geo=enriched_data.get("geo"),
                
                # Metadata - convert datetime to ISO 8601 string
                ingested_at=datetime.now(timezone.utc).isoformat()
            )
            
            # Step 3: Store the enriched news
            await self.repository.save_news(final_output)
            
            return final_output
            
        except Exception as e:
            print(f"Error during news ingestion: {str(e)}")
            raise Exception(f"News ingestion failed: {str(e)}")
    
    async def get_news_by_id(self, article_id: str) -> Optional[FinalNewsOutput]:
        """
        Retrieve a news article by its unique ID.
        
        Args:
            article_id: The unique UUID identifier
            
        Returns:
            Complete news article or None if not found
        """
        return await self.repository.get_news_by_id(article_id)
    
    async def get_all_news(self, limit: int = 100, offset: int = 0) -> list[FinalNewsOutput]:
        """
        Retrieve all news articles with pagination.
        
        Args:
            limit: Maximum number of articles to return
            offset: Number of articles to skip
            
        Returns:
            List of news articles
        """
        return await self.repository.get_all_news(limit=limit, offset=offset)
    
    async def get_news_count(self) -> int:
        """
        Get the total count of stored news articles.
        
        Returns:
            Total number of articles
        """
        return await self.repository.get_news_count()


def get_ingestion_service(db_session: AsyncSession) -> IngestionService:
    """
    Factory function to create an ingestion service instance.
    
    Args:
        db_session: Database session
        
    Returns:
        IngestionService instance
    """
    return IngestionService(db_session)

