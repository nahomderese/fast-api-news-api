"""
Handles saving and retrieving news articles from PostgreSQL database.
"""
from typing import Optional, List
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from swen_ai_pipeline.models.data_models import FinalNewsOutput
from swen_ai_pipeline.db.models import NewsArticle


class NewsRepository:
    """
    Repository for news article data access using PostgreSQL.
    
    This implementation uses SQLAlchemy with async PostgreSQL for production-ready
    data persistence, following the Repository pattern for clean separation of concerns.
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.
        
        Args:
            session: SQLAlchemy async session
        """
        self.session = session
    
    async def save_news(self, news: FinalNewsOutput) -> FinalNewsOutput:
        """
        Save a news article to the database.
        
        Args:
            news: The enriched news article to save
            
        Returns:
            The saved news article
            
        Raises:
            Exception: If save operation fails
        """
        try:
            # Check if article already exists (use UUID as slug for now)
            existing = await self.get_news_by_id(news.id)
            
            if existing:
                # Update existing article
                stmt = select(NewsArticle).where(NewsArticle.slug == news.id)
                result = await self.session.execute(stmt)
                db_article = result.scalar_one()
                
                # Update fields
                db_article.title = news.title
                db_article.body = news.body
                db_article.source_url = news.source_url
                db_article.author = news.publisher
                db_article.published_date = news.published_at
                db_article.summary = news.summary
                db_article.tags = news.tags
                db_article.sentiment_label = news.context.social_sentiment if news.context else "neutral"
                db_article.sentiment_score = 0.0  
                db_article.images = [] 
                db_article.videos = [] 
                db_article.relevance_score = news.relevance_score
                
                # Update SWEN schema fields
                if news.media:
                    db_article.featured_image_url = news.media.featured_image_url
                    db_article.related_video_url = news.media.related_video_url
                    db_article.media_justification = news.media.media_justification
                
                if news.context:
                    db_article.wikipedia_snippet = news.context.wikipedia_snippet
                    db_article.search_trend = news.context.search_trend
                
                if news.geo:
                    db_article.geo_lat = news.geo.lat
                    db_article.geo_lng = news.geo.lng
                    db_article.map_url = news.geo.map_url
            else:
                # Create new article (use UUID as slug)
                db_article = NewsArticle(
                    slug=news.id,  # Use UUID as slug
                    title=news.title,
                    body=news.body,
                    source_url=news.source_url,
                    author=news.publisher,
                    published_date=news.published_at,
                    summary=news.summary,
                    tags=news.tags,
                    sentiment_label=news.context.social_sentiment if news.context else "neutral",
                    sentiment_score=0.0,  
                    images=[],  
                    videos=[],  
                    relevance_score=news.relevance_score,
                    # SWEN schema fields
                    featured_image_url=news.media.featured_image_url if news.media else None,
                    related_video_url=news.media.related_video_url if news.media else None,
                    media_justification=news.media.media_justification if news.media else None,
                    wikipedia_snippet=news.context.wikipedia_snippet if news.context else None,
                    search_trend=news.context.search_trend if news.context else None,
                    geo_lat=news.geo.lat if news.geo else None,
                    geo_lng=news.geo.lng if news.geo else None,
                    map_url=news.geo.map_url if news.geo else None
                )
                self.session.add(db_article)
            
            await self.session.flush()
            return news
        except Exception as e:
            raise Exception(f"Failed to save news article: {str(e)}")
    
    async def get_news_by_id(self, article_id: str) -> Optional[FinalNewsOutput]:
        """
        Retrieve a news article by its unique ID.
        
        Args:
            article_id: The unique UUID identifier
            
        Returns:
            The news article if found, None otherwise
        """
        # In the database, we store the UUID as the slug field
        stmt = select(NewsArticle).where(NewsArticle.slug == article_id)
        result = await self.session.execute(stmt)
        db_article = result.scalar_one_or_none()
        
        if not db_article:
            return None
        
        return self._to_output_model(db_article)
    
    async def get_news_by_slug(self, slug: str) -> Optional[FinalNewsOutput]:
        """
        Legacy method - retrieve a news article by its slug.
        Now redirects to get_news_by_id for backward compatibility.
        
        Args:
            slug: The unique slug/ID identifier
            
        Returns:
            The news article if found, None otherwise
        """
        return await self.get_news_by_id(slug)
    
    async def get_all_news(self, limit: int = 100, offset: int = 0) -> List[FinalNewsOutput]:
        """
        Retrieve all news articles with pagination support.
        
        Args:
            limit: Maximum number of articles to return
            offset: Number of articles to skip
            
        Returns:
            List of news articles, sorted by ingestion date (newest first)
        """
        stmt = (
            select(NewsArticle)
            .order_by(NewsArticle.ingested_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        db_articles = result.scalars().all()
        
        return [self._to_output_model(article) for article in db_articles]
    
    async def get_news_count(self) -> int:
        """
        Get the total count of stored news articles.
        
        Returns:
            Total number of articles in the repository
        """
        stmt = select(func.count()).select_from(NewsArticle)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def delete_news(self, slug: str) -> bool:
        """
        Delete a news article by its slug.
        
        Args:
            slug: The unique slug identifier
            
        Returns:
            True if deleted, False if not found
        """
        stmt = select(NewsArticle).where(NewsArticle.slug == slug)
        result = await self.session.execute(stmt)
        db_article = result.scalar_one_or_none()
        
        if not db_article:
            return False
        
        await self.session.delete(db_article)
        await self.session.flush()
        return True
    
    async def news_exists(self, slug: str) -> bool:
        """
        Check if a news article exists by its slug.
        
        Args:
            slug: The unique slug identifier
            
        Returns:
            True if exists, False otherwise
        """
        stmt = select(func.count()).select_from(NewsArticle).where(NewsArticle.slug == slug)
        result = await self.session.execute(stmt)
        count = result.scalar_one()
        return count > 0
    
    async def search_news(self, query: str, limit: int = 50) -> List[FinalNewsOutput]:
        """
        Search news articles by query string.
        Searches in title, body, summary, and tags.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching news articles
        """
        search_term = f"%{query}%"
        
        stmt = (
            select(NewsArticle)
            .where(
                or_(
                    NewsArticle.title.ilike(search_term),
                    NewsArticle.body.ilike(search_term),
                    NewsArticle.summary.ilike(search_term),
                    NewsArticle.tags.cast(str).ilike(search_term)
                )
            )
            .order_by(NewsArticle.relevance_score.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        db_articles = result.scalars().all()
        
        return [self._to_output_model(article) for article in db_articles]
    
    def _to_output_model(self, db_article: NewsArticle) -> FinalNewsOutput:
        """
        Convert database model to output model.
        
        Args:
            db_article: Database article model
            
        Returns:
            FinalNewsOutput model for API responses
        """
        from swen_ai_pipeline.models.data_models import (
            EnrichedNewsMedia, EnrichedNewsContext, Geo
        )
        
        # Reconstruct enriched objects from stored data
        media = EnrichedNewsMedia(
            featured_image_url=db_article.featured_image_url,
            related_video_url=db_article.related_video_url,
            media_justification=db_article.media_justification
        )
        
        context = EnrichedNewsContext(
            wikipedia_snippet=db_article.wikipedia_snippet,
            social_sentiment=db_article.sentiment_label,
            search_trend=db_article.search_trend
        )
        
        geo = Geo(
            lat=db_article.geo_lat,
            lng=db_article.geo_lng,
            map_url=db_article.map_url
        )
        
        return FinalNewsOutput(
            id=db_article.slug,  # slug field stores the UUID
            title=db_article.title,
            body=db_article.body,
            source_url=db_article.source_url,
            publisher=db_article.author,
            published_at=db_article.published_date,
            summary=db_article.summary,
            tags=db_article.tags,
            relevance_score=db_article.relevance_score,
            media=media,
            context=context,
            geo=geo,
            ingested_at=db_article.ingested_at.isoformat() if hasattr(db_article.ingested_at, 'isoformat') else str(db_article.ingested_at)
        )


def get_repository(session: AsyncSession) -> NewsRepository:
    """
    Factory function to create a repository instance.
    
    Args:
        session: Database session
        
    Returns:
        NewsRepository instance
    """
    return NewsRepository(session)

