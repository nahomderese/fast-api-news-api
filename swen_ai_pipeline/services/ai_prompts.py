"""
AI prompt templates for different enrichment tasks.
"""
from typing import Dict, Any

from .ai_utils import (
    format_african_cities_reference,
    create_media_validation_prompt,
    create_geo_validation_prompt,
    create_content_quality_prompt,
    create_tag_quality_prompt
)


class AIPrompts:
    """Centralized prompt templates for AI operations."""
    
    @staticmethod
    def summary_prompt(title: str, body: str) -> str:
        """Generate summary prompt."""
        return f"""You are a news editor for SWEN, focusing on African market relevance. Highlight connections to Africa, sustainability, and regional impact.

Summarize this news article in 2-3 concise sentences, emphasizing relevance to African audiences and markets.

Title: {title}
Content: {body}"""
    
    @staticmethod
    def tags_prompt(title: str, body: str) -> str:
        """Generate tags prompt."""
        return f"""You are a content strategist for SWEN focusing on African market relevance.

{create_tag_quality_prompt()}

Title: {title}
Content: {body[:800]}

Return ONLY a JSON array of hashtag strings (with # prefix)."""
    
    @staticmethod
    def relevance_score_prompt(title: str, body: str) -> str:
        """Generate relevance score prompt."""
        return f"""You are SWEN's African market analyst. Score articles based on their relevance and value to African audiences.

Rate this news article's relevance to African audiences on a scale of 0.0 to 1.0.

Scoring criteria (African audience focus):
- Direct impact on African countries/regions: HIGH weight
- Relevance to African sustainability, green energy, climate: HIGH weight
- African business, economy, trade implications: HIGH weight
- Regional development, infrastructure, technology: MEDIUM weight
- Global news with African connections: MEDIUM weight
- General news with minimal African relevance: LOW weight

Return ONLY a number between 0.0 and 1.0, nothing else.

Title: {title}
Content: {body[:800]}"""
    
    @staticmethod
    def media_discovery_prompt(title: str, body: str, tags: list) -> str:
        """Generate media discovery prompt."""
        return f"""You are SWEN's media curator with access to real media databases.

{create_media_validation_prompt()}

Analyze this article and provide real media URLs:

Title: {title}
Tags: {', '.join(tags)}
Content: {body[:500]}

Return ONLY a JSON object:
{{
  "featured_image_url": "https://images.unsplash.com/photo-XXXXX?w=800&q=80",
  "related_video_url": "https://www.youtube.com/watch?v=REAL_VIDEO_ID",
  "media_justification": "Detailed explanation of why these media items are relevant to African audiences"
}}"""
    
    @staticmethod
    def context_extraction_prompt(title: str, body: str) -> str:
        """Generate context extraction prompt."""
        return f"""You are SWEN's African context analyst. Generate RICH, HIGH-QUALITY contextual analysis.

{create_content_quality_prompt()}

Title: {title}
Content: {body[:1200]}

Analyze deeply and return ONLY a JSON object:
{{
  "wikipedia_snippet": "Rich, detailed background context with African relevance (50-100 words)",
  "social_sentiment": "positive",
  "search_trend": "rising"
}}"""
    
    @staticmethod
    def geo_extraction_prompt(title: str, body: str) -> str:
        """Generate geographic extraction prompt."""
        return f"""You are SWEN's geographic analyst with access to coordinate databases.

{create_geo_validation_prompt()}

Title: {title}
Content: {body[:1200]}

Analyze the content carefully and return ONLY a JSON object:
{{
  "lat": -1.286389,
  "lng": 36.817223,
  "map_url": "https://www.google.com/maps?q=-1.286389,36.817223",
  "location_name": "Nairobi, Kenya"
}}

Return ONLY the JSON object."""
    
    @staticmethod
    def unified_enrichment_prompt(title: str, body: str) -> str:
        """Generate unified enrichment prompt."""
        return f"""You are SWEN's AI enrichment engine. Generate comprehensive, HIGH-QUALITY analysis prioritizing African market relevance.

CRITICAL REQUIREMENTS - NO PLACEHOLDERS:
1. Tags: 3-5 COHERENT, SPECIFIC hashtags reflecting actual article content (NOT generic)
2. Media URLs: REAL working URLs (Unsplash photo IDs, real YouTube video IDs)
3. Geo Coordinates: ACCURATE lat/lng for locations mentioned in the article
4. Context: Rich, detailed, high-quality content
5. Relevance Score: Based on African audience importance (0.0-1.0)

TAG REQUIREMENTS:
- Generate exactly 3-5 tags (not 8 or more)
- Use specific, relevant hashtags (e.g., #ZambiaMining, #CriticalMinerals, #SupplyChainDiversification)
- Include country/region names when relevant
- Focus on key themes: mining, trade, technology, sustainability, etc.
- Use proper CamelCase formatting

MEDIA REQUIREMENTS (E-E-A-T Authority):
- Find ONE Primary Image: High-resolution, relevant image
- Find ONE Primary Video: From authoritative sources ONLY (Reuters, BBC, NASA, WHO, UN, etc.)
- featured_image_url: Use format "https://images.unsplash.com/photo-XXXXX?w=800&q=80" with real photo ID
- image_caption: Concise journalistic caption (max 15 words)
- related_video_url: Use format "https://www.youtube.com/watch?v=VIDEO_ID" from official channels ONLY
- video_caption: Concise journalistic caption (max 15 words) - only if video found
- Video Fallback: If NO authoritative video exists, set video_url to empty string ("")
- media_justification: Detailed explanation (50+ words) including E-E-A-T authority justification
- NO search results URLs, NO placeholder URLs, NO personal blogs

GEO REQUIREMENTS:
- Extract PRIMARY location from article (city/country/specific site)
- Provide accurate coordinates (reference common African cities)
- Generate proper Google Maps URL: "https://www.google.com/maps?q=LAT,LNG"
- If NO location mentioned, set all geo fields to null

Common African coordinates:
{format_african_cities_reference()}

Title: {title}
Content: {body[:1500]}

Return ONLY valid JSON:
{{
  "summary": "2-3 sentences emphasizing African relevance",
  "tags": ["#SpecificCountry", "#SpecificTheme", "#RelevantTopic", "#AfricanContext"],
  "relevance_score": 0.85,
  "featured_image_url": "https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800&q=80",
  "image_caption": "High-resolution image showing relevant content",
  "related_video_url": "https://www.youtube.com/watch?v=zn8o_DwUwFk",
  "video_caption": "Authoritative video from official source",
  "media_justification": "Detailed explanation of media selection for African audiences, including E-E-A-T authority justification, relevance to article content, and visual elements that enhance understanding",
  "wikipedia_snippet": "Rich contextual background (50-100 words)",
  "social_sentiment": "positive",
  "search_trend": "rising",
  "geo_lat": -1.286389,
  "geo_lng": 36.817223,
  "geo_map_url": "https://www.google.com/maps?q=-1.286389,36.817223"
}}

IMPORTANT: If no authoritative video found, use:
"related_video_url": "",
"video_caption": """""
