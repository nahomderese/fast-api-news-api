"""
This module defines all JSON structures for input, processing, and output.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from uuid import uuid4


class RawNewsInput(BaseModel):
    """
    Input model for raw news data ingestion.
    Represents the minimal required fields for news processing.
    Accepts both 'author'/'published_date' and 'publisher'/'published_at' field names.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    title: str = Field(..., description="News article title")
    body: str = Field(..., description="Full news article body text")
    source_url: HttpUrl = Field(..., description="Original news source URL")
    author: Optional[str] = Field(
        None, 
        description="Article author/publisher name",
        alias="publisher",
        validation_alias="publisher"
    )
    published_date: Optional[str] = Field(
        None, 
        description="Original publication date (ISO 8601)",
        alias="published_at",
        validation_alias="published_at"
    )


class EnrichedNewsMedia(BaseModel):
    """
    Media enrichment model containing AI-discovered media URLs.
    Compliant with SWEN schema requirements.
    """
    model_config = ConfigDict(populate_by_name=True, exclude_none=True)
    
    search_query: Optional[str] = Field(
        None,
        description="AI-generated search query used to discover media"
    )
    featured_image_url: Optional[str] = Field(
        None, 
        description="AI-discovered featured image URL relevant to the article"
    )
    image_caption: Optional[str] = Field(
        None, 
        description="Concise journalistic caption for the image (max 15 words)"
    )
    related_video_url: Optional[str] = Field(
        None, 
        description="AI-discovered related video URL from authoritative source"
    )
    video_caption: Optional[str] = Field(
        None, 
        description="Concise journalistic caption for the video (max 15 words)"
    )
    media_justification: Optional[str] = Field(
        None, 
        description="AI-generated rationale for media selection"
    )


class EnrichedNewsContext(BaseModel):
    """
    Contextual enrichment model containing AI-generated context information.
    Compliant with SWEN schema requirements.
    """
    model_config = ConfigDict(populate_by_name=True, exclude_none=True)
    
    wikipedia_snippet: Optional[str] = Field(
        None, 
        description="Relevant Wikipedia snippet for context"
    )
    social_sentiment: Optional[str] = Field(
        None, 
        description="AI-analyzed social sentiment (positive/negative/neutral)"
    )
    search_trend: Optional[str] = Field(
        None, 
        description="AI-analyzed search trend information"
    )


class Geo(BaseModel):
    """
    Geographic coordinates and map information.
    Compliant with SWEN schema requirements.
    """
    model_config = ConfigDict(populate_by_name=True, exclude_none=True)
    
    lat: Optional[float] = Field(
        None, 
        description="Latitude coordinate"
    )
    lng: Optional[float] = Field(
        None, 
        description="Longitude coordinate"
    )
    map_url: Optional[str] = Field(
        None, 
        description="URL to map location"
    )


class FinalNewsOutput(BaseModel):
    """
    Complete enriched news output model.
    Represents the final JSON structure stored and returned by the API.
    Compliant with SWEN schema requirements - exactly 17 fields.
    """
    model_config = ConfigDict(populate_by_name=True, exclude_none=True)
    
    # Unique identifier (UUID)
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier (UUID)",
        serialization_alias="id"
    )
    
    # Original fields
    title: str = Field(..., description="News article title")
    body: str = Field(..., description="Full news article body text")
    source_url: str = Field(..., description="Original news source URL", serialization_alias="source_url")
    publisher: Optional[str] = Field(
        None, 
        description="Article publisher/author name",
        serialization_alias="publisher"
    )
    published_at: Optional[str] = Field(
        None, 
        description="Original publication date (ISO 8601)",
        serialization_alias="published_at"
    )
    
    # AI-generated core fields
    summary: str = Field(..., description="AI-generated summary of the article")
    tags: List[str] = Field(
        default_factory=list, 
        description="AI-generated tags/categories"
    )
    relevance_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="AI-calculated relevance score (0.0 to 1.0)"
    )
    
    # Nested enriched objects
    media: EnrichedNewsMedia = Field(
        default_factory=EnrichedNewsMedia, 
        description="Media enrichment data"
    )
    context: EnrichedNewsContext = Field(
        default_factory=EnrichedNewsContext, 
        description="Contextual enrichment data"
    )
    geo: Geo = Field(
        default_factory=Geo,
        description="Geographic information"
    )
    
    # Metadata
    ingested_at: str = Field(
        ...,
        description="Timestamp when the article was ingested (ISO 8601)"
    )


class NewsSummary(BaseModel):
    """
    Summary model for list endpoints.
    Contains only essential fields for news listing.
    """
    model_config = ConfigDict(populate_by_name=True, exclude_none=True)
    
    id: str = Field(..., description="Unique identifier (UUID)")
    title: str = Field(..., description="News article title")
    summary: str = Field(..., description="AI-generated summary")
    tags: List[str] = Field(default_factory=list, description="Article tags")
    relevance_score: float = Field(..., description="Relevance score")
    published_at: Optional[str] = Field(None, description="Publication date (ISO 8601)", serialization_alias="published_at")
    ingested_at: str = Field(..., description="Ingestion timestamp (ISO 8601)")
    featured_image_url: Optional[str] = Field(
        None, 
        description="Featured image URL"
    )


class NewsListResponse(BaseModel):
    """
    Response model for the GET /api/v1/news endpoint.
    """
    total: int = Field(..., description="Total number of news items")
    items: List[NewsSummary] = Field(
        default_factory=list, 
        description="List of news summaries"
    )


class IngestionResponse(BaseModel):
    """
    Response model for the POST /api/v1/ingest endpoint.
    """
    status: str = Field(..., description="Ingestion status")
    message: str = Field(..., description="Status message")
    id: str = Field(..., description="Generated UUID for the article")
    data: FinalNewsOutput = Field(..., description="Complete enriched news data")

