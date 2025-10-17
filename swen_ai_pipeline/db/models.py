"""
SQLAlchemy database models for news articles.
"""
from datetime import datetime
from typing import List
from sqlalchemy import String, Text, Float, DateTime, JSON, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class NewsArticle(Base):
    """
    Database model for news articles with AI enrichments.
    
    This model represents the complete news article with:
    - Original content (title, body)
    - AI-generated enhancements (summary, tags, sentiment)
    - Media content (images, videos)
    - Metadata (timestamps, relevance score)
    """
    __tablename__ = "news_articles"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Unique slug identifier
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    
    # Original content
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    published_date: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # AI-generated content
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    
    # Sentiment analysis
    sentiment_label: Mapped[str] = mapped_column(String(50), nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Media content (SWEN schema fields)
    featured_image_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    related_video_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    media_justification: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Context content (SWEN schema fields)
    wikipedia_snippet: Mapped[str] = mapped_column(Text, nullable=True)
    search_trend: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Geographic data (SWEN schema fields)
    geo_lat: Mapped[float] = mapped_column(Float, nullable=True)
    geo_lng: Mapped[float] = mapped_column(Float, nullable=True)
    map_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    # Legacy media fields (kept for backward compatibility)
    images: Mapped[List[dict]] = mapped_column(JSON, nullable=False, default=list)
    videos: Mapped[List[dict]] = mapped_column(JSON, nullable=False, default=list)
    
    # Metadata
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def __repr__(self) -> str:
        """String representation of the news article."""
        return f"<NewsArticle(slug='{self.slug}', title='{self.title[:50]}...')>"
    
    def to_dict(self) -> dict:
        """
        Convert the model to a dictionary suitable for API responses.
        
        Returns:
            Dictionary representation of the news article
        """
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "body": self.body,
            "source_url": self.source_url,
            "author": self.author,
            "published_date": self.published_date,
            "summary": self.summary,
            "tags": self.tags,
            "sentiment": {
                "label": self.sentiment_label,
                "score": self.sentiment_score
            },
            "images": self.images,
            "videos": self.videos,
            "relevance_score": self.relevance_score,
            "ingested_at": self.ingested_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

