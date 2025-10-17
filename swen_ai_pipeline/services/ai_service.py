"""
Handles all AI operations including LLM calls and media discovery.
Refactored for modularity and clean code organization.
"""
import json
from typing import List, Dict, Any

from google import genai

from swen_ai_pipeline.models.data_models import (
    RawNewsInput,
    EnrichedNewsMedia,
    EnrichedNewsContext,
    Geo
)
from swen_ai_pipeline.core.config import settings
from .ai_constants import DEFAULT_FALLBACKS, CONTENT_LIMITS
from .ai_utils import (
    clean_json_response,
    validate_coordinates,
    validate_media_url,
    validate_content_quality,
    parse_json_safely,
    create_geo_from_coordinates,
    get_fallback_media_urls,
    get_fallback_content,
    create_media_validation_prompt
)
from .ai_prompts import AIPrompts
from .brave_search_service import brave_search_service


class AIService:
    """
    AI Service for news enrichment using Google Gemini.
    Handles summary generation, tagging, context extraction, and media discovery.
    """
    
    def __init__(self):
        """Initialize the AI service with Gemini client."""
        self.use_mock = settings.use_mock_ai
        self.client = None
        self.model_id = settings.gemini_model
        
        if not self.use_mock:
            self.client = genai.Client(api_key=settings.gemini_api_key,)
    
    async def generate_summary(self, title: str, body: str) -> str:
        """Generate an AI-powered summary with African audience focus."""
        if self.use_mock:
            return ' '.join(body.split()[:30]) + "..."
        
        prompt = AIPrompts.summary_prompt(title, body)
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text.strip()
    
    async def generate_tags(self, title: str, body: str) -> List[str]:
        """Generate coherent, relevant African-localized hashtags for the article."""
        if self.use_mock:
            return ["#Africa", "#News", "#Technology"]
        
        prompt = AIPrompts.tags_prompt(title, body)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            content = response.text.strip()
            cleaned_content = clean_json_response(content)
            
            tags = json.loads(cleaned_content)
            if isinstance(tags, list) and len(tags) > 0:
                # Ensure we have 3-5 tags, prioritizing the most relevant ones
                if len(tags) < CONTENT_LIMITS["min_tags"]:
                    # If we have fewer than 3 tags, pad with relevant fallbacks
                    while len(tags) < CONTENT_LIMITS["min_tags"]:
                        tags.append("#Africa")
                return tags[:CONTENT_LIMITS["max_tags"]]
            return DEFAULT_FALLBACKS["tags"]
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Tag generation error: {e}")
            return DEFAULT_FALLBACKS["tags"]
    
    async def calculate_relevance_score(self, title: str, body: str) -> float:
        """Calculate relevance score based on African audience importance."""
        if self.use_mock:
            return DEFAULT_FALLBACKS["relevance_score"]
        
        prompt = AIPrompts.relevance_score_prompt(title, body)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            score_str = response.text.strip()
            score = float(score_str)
            return min(max(score, 0.0), 1.0)
        except (ValueError, AttributeError, Exception):
            return DEFAULT_FALLBACKS["relevance_score"]
    
    
    
    async def generate_media_search_query(self, title: str, body: str) -> str:
        """
        Generate a concise, high-quality search query for media discovery.
        
        Args:
            title: Article title
            body: Article body text
            
        Returns:
            Concise search query string
        """
        if self.use_mock:
            return f"{title[:50]}"
        
        prompt = f"""You are SWEN's media search query generator. Generate ONE concise, high-quality search query for finding relevant images and videos.

REQUIREMENTS:
1. Generate a search query that is 3-7 words maximum
2. Focus on the main topic/subject of the article
3. Include relevant keywords that will find authoritative media
4. Make it specific and descriptive
5. Return ONLY the search query string (no quotes, no JSON, just the query)

Article Title: {title}
Article Content: {body[:800]}

Generate the optimal search query:"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            query = response.text.strip()
            # Remove any quotes that might be added
            query = query.strip('"').strip("'")
            # Limit to reasonable length
            words = query.split()
            if len(words) > 7:
                query = " ".join(words[:7])
            return query
        except Exception as e:
            print(f"Search query generation error: {e}")
            # Fallback to title
            return title[:100]
    
    async def discover_media(self, title: str, body: str, tags: List[str]) -> EnrichedNewsMedia:
        """
        Discover high-quality media using Brave Search API.
        
        Process:
        1. AI determines the relevant country for the article
        2. AI generates optimal search query
        3. Search Brave API for images and videos (with country-specific results)
        4. Return first result from each
        """
        import logging

        logger = logging.getLogger("swen.ai_service.discover_media")
        logger.debug("Starting discover_media with title='%s', tags=%s", title, tags)
        if self.use_mock:
            logger.debug("Using mock mode for discover_media.")
            return EnrichedNewsMedia(
                search_query="African development technology",
                featured_image_url=DEFAULT_FALLBACKS["featured_image_url"],
                image_caption="High-quality image relevant to African development",
                related_video_url=DEFAULT_FALLBACKS["related_video_url"],
                video_caption="Authoritative video content",
                media_justification=DEFAULT_FALLBACKS["media_justification"]
            )
        
        try:
            logger.debug("Generating media search query.")
            search_query = await self.generate_media_search_query(title, body)
            logger.debug("Generated search query: %r", search_query)
            
            logger.debug("Calling Brave Search Service discover_media with search_query: %r", search_query)
            media_results = await brave_search_service.discover_media(search_query)
            logger.debug("Brave Search Service results: %r", media_results)
            
            image_url = media_results.get("image_url")
            video_url = media_results.get("video_url")

            logger.debug("Discovered image_url: %r, video_url: %r", image_url, video_url)
            
            # Generate captions based on the results
            image_caption = None
            video_caption = None

            if image_url and media_results.get("image_metadata"):
                img_title = media_results["image_metadata"].get("title", "")
                logger.debug("Image metadata title: %r", img_title)
                if img_title:
                    words = img_title.split()
                    image_caption = " ".join(words[:15]) if len(words) > 15 else img_title

            if video_url and media_results.get("video_metadata"):
                vid_title = media_results["video_metadata"].get("title", "")
                logger.debug("Video metadata title: %r", vid_title)
                if vid_title:
                    words = vid_title.split()
                    video_caption = " ".join(words[:15]) if len(words) > 15 else vid_title

            # No country_code variable defined, remove from justification
            justification = f"Media content discovered using search query '{search_query}' via Brave Search API. "
            if image_url:
                justification += f"Image sourced from authoritative content providers. "
            if video_url:
                justification += f"Video content from verified sources. "
            justification += "Selected to provide visual context relevant to the article's themes and regional audience interests."
            logger.debug("Generated justification: %s", justification)
            
            # Use fallbacks if no results found
            if not image_url:
                logger.debug("No image found, using fallback image.")
                image_url = DEFAULT_FALLBACKS["featured_image_url"]
                image_caption = "High-quality image relevant to African development"
            
            if not video_url:
                logger.debug("No video found, falling back to empty string and None for caption.")
                video_url = ""
                video_caption = None
            
            result = EnrichedNewsMedia(
                search_query=search_query,
                featured_image_url=image_url,
                image_caption=image_caption,
                related_video_url=video_url if video_url else "",
                video_caption=video_caption,
                media_justification=justification
            )
            logger.debug("Returning EnrichedNewsMedia: %r", result)
            return result
            
        except Exception as e:
            logger.exception("Media discovery error")
            return EnrichedNewsMedia(
                search_query=title[:100],
                featured_image_url=DEFAULT_FALLBACKS["featured_image_url"],
                image_caption="High-quality image relevant to African development",
                related_video_url="",
                video_caption=None,
                media_justification=DEFAULT_FALLBACKS["media_justification"]
            )
    
    async def extract_context(self, title: str, body: str) -> EnrichedNewsContext:
        """Extract rich, high-quality contextual information with African market focus."""
        if self.use_mock:
            return EnrichedNewsContext(
                wikipedia_snippet=DEFAULT_FALLBACKS["wikipedia_snippet"],
                social_sentiment=DEFAULT_FALLBACKS["social_sentiment"],
                search_trend=DEFAULT_FALLBACKS["search_trend"]
            )
        
        prompt = f"""You are SWEN's African context analyst. Generate RICH, HIGH-QUALITY contextual analysis.

CRITICAL REQUIREMENTS:
1. Wikipedia Snippet: Write 50-100 words of insightful background context
   - Emphasize African relevance and regional impact
   - Include specific facts, statistics, or historical context
   - Make it informative and valuable for African readers
   
2. Social Sentiment: Analyze from African audience perspective
   - "positive" - good news for Africa, opportunities, progress
   - "negative" - challenges, setbacks, concerns for Africa
   - "neutral" - balanced or informational
   
3. Search Trend: Assess trending status
   - "viral" - extremely high interest, widespread discussion
   - "rising" - growing interest and searches
   - "stable" - consistent interest
   - "declining" - decreasing interest

Title: {title}
Content: {body[:1200]}

Analyze deeply and return ONLY a JSON object:
{{
  "wikipedia_snippet": "Rich, detailed background context with African relevance (50-100 words)",
  "social_sentiment": "positive",
  "search_trend": "rising"
}}

NO generic responses. Make it specific and valuable."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            content = response.text.strip()
            # Remove markdown if present
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            data = json.loads(content)
            
            snippet = data.get("wikipedia_snippet", "")
            if not snippet or len(snippet) < 20:  # Ensure quality content
                snippet = "This article provides important insights relevant to African markets, regional development, and continental progress."
            
            return EnrichedNewsContext(
                wikipedia_snippet=snippet,
                social_sentiment=data.get("social_sentiment", "neutral"),
                search_trend=data.get("search_trend", "stable")
            )
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"Context extraction error: {e}")
            return EnrichedNewsContext(
                wikipedia_snippet="This article covers topics of significance to African audiences and regional development.",
                social_sentiment="neutral",
                search_trend="stable"
            )
    
    async def extract_geo(self, title: str, body: str) -> Geo:
        """Extract and calculate precise geographic coordinates from the article."""
        if self.use_mock:
            return Geo(
                lat=-1.286389,
                lng=36.817223,
                map_url="https://www.google.com/maps?q=-1.286389,36.817223"
            )
        
        prompt = f"""You are SWEN's geographic analyst with access to coordinate databases.

CRITICAL REQUIREMENTS:
1. Identify the PRIMARY location mentioned in the article (country, city, region)
2. Provide ACCURATE latitude and longitude coordinates for that location
3. Generate a proper Google Maps URL using those coordinates
4. If multiple locations are mentioned, choose the most relevant one
5. Use real coordinates (not approximations)

Common African locations reference:
- Nairobi, Kenya: -1.286389, 36.817223
- Lagos, Nigeria: 6.5244, 3.3792
- Johannesburg, South Africa: -26.2041, 28.0473
- Cairo, Egypt: 30.0444, 31.2357
- Addis Ababa, Ethiopia: 9.0320, 38.7469
- Accra, Ghana: 5.6037, -0.1870
- Dar es Salaam, Tanzania: -6.7924, 39.2083
- Kigali, Rwanda: -1.9536, 30.0606

Title: {title}
Content: {body[:1200]}

Analyze the content carefully and return ONLY a JSON object:
{{
  "lat": -1.286389,
  "lng": 36.817223,
  "map_url": "https://www.google.com/maps?q=-1.286389,36.817223",
  "location_name": "Nairobi, Kenya"
}}

If NO specific location is mentioned, return: {{"lat": null, "lng": null, "map_url": null}}

Return ONLY the JSON object."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            content = response.text.strip()
            # Remove markdown if present
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            data = json.loads(content)
            
            lat = data.get("lat")
            lng = data.get("lng")
            
            # Validate coordinates
            if lat is not None and lng is not None:
                # Ensure coordinates are within valid ranges
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    map_url = f"https://www.google.com/maps?q={lat},{lng}"
                    return Geo(lat=lat, lng=lng, map_url=map_url)
            
            # If coordinates invalid or missing, return empty geo
            return Geo()
            
        except (json.JSONDecodeError, KeyError, AttributeError, ValueError) as e:
            print(f"Geo extraction error: {e}")
            return Geo()
    
    async def unified_enrich(self, title: str, body: str) -> Dict[str, Any]:
        """Generate complete enrichment in single LLM call with African focus - HIGH QUALITY CONTENT ONLY."""
        prompt = f"""You are SWEN's AI enrichment engine. Generate comprehensive, HIGH-QUALITY analysis prioritizing African market relevance.

CRITICAL REQUIREMENTS - NO PLACEHOLDERS:
1. Tags: COHERENT hashtags reflecting actual article content (NOT generic)
2. Media URLs: REAL working URLs (Unsplash photo IDs, real YouTube video IDs)
3. Geo Coordinates: ACCURATE lat/lng for locations mentioned in the article
4. Context: Rich, detailed, high-quality content
5. Relevance Score: Based on African audience importance (0.0-1.0)

MEDIA REQUIREMENTS:
- featured_image_url: Use format "https://images.unsplash.com/photo-XXXXX?w=800&q=80" with real photo ID
- related_video_url: Use format "https://www.youtube.com/watch?v=VIDEO_ID" with real video ID
- NO search results URLs, NO placeholder URLs

GEO REQUIREMENTS:
- Extract PRIMARY location from article (city/country)
- Provide accurate coordinates (reference common African cities)
- Generate proper Google Maps URL: "https://www.google.com/maps?q=LAT,LNG"
- If NO location mentioned, set all geo fields to null

Common African coordinates:
- Nairobi: -1.286389, 36.817223
- Lagos: 6.5244, 3.3792
- Johannesburg: -26.2041, 28.0473
- Cairo: 30.0444, 31.2357

Title: {title}
Content: {body[:1500]}

Return ONLY valid JSON:
{{
  "summary": "2-3 sentences emphasizing African relevance",
  "tags": ["#Specific", "#Coherent", "#Tags", "#NotGeneric"],
  "relevance_score": 0.85,
  "featured_image_url": "https://images.unsplash.com/photo-XXXXX?w=800&q=80",
  "related_video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "media_justification": "Detailed explanation of media selection for African audiences",
  "wikipedia_snippet": "Rich contextual background (50-100 words)",
  "social_sentiment": "positive",
  "search_trend": "rising",
  "geo_lat": -1.286389,
  "geo_lng": 36.817223,
  "geo_map_url": "https://www.google.com/maps?q=-1.286389,36.817223"
}}"""
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        content = response.text.strip()
        # Remove markdown if present
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        return json.loads(content)
    
    async def enrich_news(self, raw_input: RawNewsInput) -> Dict[str, Any]:
        """
        Orchestrate the complete AI enrichment pipeline for a news article.
        
        Media discovery now uses Brave Search API:
        1. AI generates a concise search query from the article
        2. Query is used to search Brave's Image and Video verticals
        3. First result from each is selected
        """
        # Use individual calls with Brave Search integration
        summary = await self.generate_summary(raw_input.title, raw_input.body)
        tags = await self.generate_tags(raw_input.title, raw_input.body)
        relevance_score = await self.calculate_relevance_score(raw_input.title, raw_input.body)
        
        # Media discovery now uses Brave Search API
        media = await self.discover_media(raw_input.title, raw_input.body, tags)
        
        context = await self.extract_context(raw_input.title, raw_input.body)
        geo = await self.extract_geo(raw_input.title, raw_input.body)
        
        return {
            "summary": summary,
            "tags": tags,
            "relevance_score": relevance_score,
            "media": media,
            "context": context,
            "geo": geo
        }
    
    def close(self):
        """Close the Gemini client to release resources."""
        if self.client:
            self.client.close()


ai_service = AIService()

