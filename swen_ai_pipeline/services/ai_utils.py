"""
Utility functions for AI service operations.
"""
import json
import re
from typing import Dict, Any, Optional, Tuple, List

from swen_ai_pipeline.models.data_models import Geo
from .ai_constants import (
    AFRICAN_CITIES_COORDINATES,
    DEFAULT_MEDIA_URLS,
    DEFAULT_FALLBACKS,
    CONTENT_LIMITS,
    COORDINATE_RANGES,
    URL_PATTERNS
)


def clean_json_response(content: str) -> str:
    """
    Clean and extract JSON from LLM response, removing markdown formatting.
    
    Args:
        content: Raw response content from LLM
        
    Returns:
        Cleaned JSON string
    """
    content = content.strip()
    
    # Remove markdown code blocks if present
    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    
    return content.strip()


def validate_coordinates(lat: Optional[float], lng: Optional[float]) -> bool:
    """
    Validate that coordinates are within valid ranges.
    
    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    if lat is None or lng is None:
        return False
    
    return (
        COORDINATE_RANGES["lat_min"] <= lat <= COORDINATE_RANGES["lat_max"] and
        COORDINATE_RANGES["lng_min"] <= lng <= COORDINATE_RANGES["lng_max"]
    )


def validate_media_url(url: str, url_type: str) -> bool:
    """
    Validate that media URL is not a placeholder or search result.
    
    Args:
        url: URL to validate
        url_type: Type of URL ('image' or 'video')
        
    Returns:
        True if URL is valid, False otherwise
    """
    if not url:
        return False
    
    if url_type == "image":
        return (
            URL_PATTERNS["unsplash_direct"] in url and
            URL_PATTERNS["unsplash_source"] not in url and
            "?w=" in url
        )
    elif url_type == "video":
        return (
            URL_PATTERNS["youtube_watch"] in url and
            URL_PATTERNS["youtube_search"] not in url and
            URL_PATTERNS["youtube_results"] not in url
        )
    
    return False


def extract_location_from_text(text: str) -> Optional[Tuple[str, float, float]]:
    """
    Extract location information from text using the cities database.
    
    Args:
        text: Text to search for locations
        
    Returns:
        Tuple of (city_name, lat, lng) if found, None otherwise
    """
    text_lower = text.lower()
    
    # Search for city names in the text
    for city_name, (lat, lng) in AFRICAN_CITIES_COORDINATES.items():
        if city_name.lower() in text_lower:
            return city_name, lat, lng
    
    return None


def create_geo_from_coordinates(lat: float, lng: float) -> Geo:
    """
    Create Geo object from coordinates with proper validation.
    
    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        
    Returns:
        Geo object with coordinates and map URL
    """
    if validate_coordinates(lat, lng):
        return Geo(
            lat=lat,
            lng=lng,
            map_url=f"https://www.google.com/maps?q={lat},{lng}"
        )
    return Geo()


def get_fallback_media_urls() -> Dict[str, str]:
    """
    Get fallback media URLs for when AI generation fails.
    
    Returns:
        Dictionary with fallback URLs
    """
    return DEFAULT_MEDIA_URLS.copy()


def get_fallback_content() -> Dict[str, Any]:
    """
    Get fallback content for when AI generation fails.
    
    Returns:
        Dictionary with fallback content
    """
    return DEFAULT_FALLBACKS.copy()


def validate_content_quality(content: str, min_length: int = CONTENT_LIMITS["min_snippet_length"]) -> bool:
    """
    Validate that content meets minimum quality requirements.
    
    Args:
        content: Content to validate
        min_length: Minimum required length
        
    Returns:
        True if content meets quality requirements
    """
    if not content:
        return False
    
    # Check for generic placeholder text
    generic_phrases = [
        "unavailable", "not available", "no context", "placeholder",
        "default", "generic", "lorem ipsum", "test content"
    ]
    
    content_lower = content.lower()
    for phrase in generic_phrases:
        if phrase in content_lower:
            return False
    
    return len(content.strip()) >= min_length


def parse_json_safely(content: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely parse JSON content with fallback handling.
    
    Args:
        content: JSON string to parse
        fallback: Fallback dictionary if parsing fails
        
    Returns:
        Parsed dictionary or fallback
    """
    try:
        cleaned_content = clean_json_response(content)
        return json.loads(cleaned_content)
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"JSON parsing error: {e}")
        return fallback


def extract_tags_from_content(content: str) -> List[str]:
    """
    Extract potential tags from content for validation.
    
    Args:
        content: Content to analyze
        
    Returns:
        List of potential tags
    """
    # Simple keyword extraction for validation
    words = re.findall(r'\b[A-Z][a-z]+\b', content)
    return [f"#{word}" for word in words[:5]]


def format_african_cities_reference() -> str:
    """
    Format the African cities reference for prompts.
    
    Returns:
        Formatted string with city coordinates
    """
    lines = []
    for city, (lat, lng) in list(AFRICAN_CITIES_COORDINATES.items())[:8]:  # Top 8 cities
        lines.append(f"- {city}: {lat}, {lng}")
    return "\n".join(lines)


def create_media_validation_prompt() -> str:
    """
    Create validation prompt for media URL generation with E-E-A-T authority requirements.
    
    Returns:
        Formatted prompt string
    """
    return f"""
CRITICAL E-E-A-T AUTHORITY REQUIREMENTS:
1. Find ONE Primary Image: Search for the single most relevant, high-resolution image
2. Find ONE Primary Video: Search for ONE authoritative video from credible sources ONLY
3. Authority Sources (E-E-A-T): Media MUST come from high-authority sources:
   - News outlets: Reuters, BBC, Al Jazeera, AFP, Bloomberg, CNN, Financial Times
   - Official bodies: NASA, WHO, UN, World Bank, government press releases
   - Educational: Universities, research institutions
   - NO personal blogs, NO unverified sources, NO placeholder content
4. Link Quality: All URLs MUST be fully qualified (https://...), publicly accessible, working links
5. Video Fallback: If NO suitable authoritative video exists, return empty string ("") for video_url
6. Image caption: Generate concise, journalistic caption (max 15 words)
7. Video caption: Generate concise, journalistic caption (max 15 words) - only if video found

URL FORMATS:
- Image: Use Unsplash format "https://images.unsplash.com/photo-XXXXX?w=800&q=80"
- Video: Use YouTube format "https://www.youtube.com/watch?v=VIDEO_ID" (from official channels ONLY)
- If no authoritative video: video_url = ""

CAPTION REQUIREMENTS:
- Maximum 15 words
- Journalistic style (factual, concise)
- Describe what's shown and relevance
- Professional tone

MEDIA JUSTIFICATION REQUIREMENTS (50+ words):
- Explain the connection to the article content
- Highlight relevance to African audiences
- Justify authority of source (E-E-A-T compliance)
- Describe visual elements that enhance understanding
- Explain why this specific authoritative source was chosen
"""


def create_geo_validation_prompt() -> str:
    """
    Create validation prompt for geographic coordinate extraction.
    
    Returns:
        Formatted prompt string
    """
    return f"""
CRITICAL REQUIREMENTS:
1. Identify the PRIMARY location mentioned in the article (country, city, region, specific site)
2. Provide ACCURATE latitude and longitude coordinates for that location
3. Generate a proper Google Maps URL using those coordinates: "https://www.google.com/maps?q=LAT,LNG"
4. If multiple locations are mentioned, choose the most relevant one
5. Use real coordinates (not approximations)
6. For specific sites (mines, facilities, etc.), use the most accurate coordinates available

Common African locations reference:
{format_african_cities_reference()}

COORDINATE ACCURACY:
- Use precise coordinates when available
- For cities, use city center coordinates
- For specific facilities, use facility coordinates
- Ensure coordinates are within valid ranges: lat (-90 to 90), lng (-180 to 180)

If NO specific location is mentioned, return: {{"lat": null, "lng": null, "map_url": null}}
"""


def create_content_quality_prompt() -> str:
    """
    Create validation prompt for high-quality content generation.
    
    Returns:
        Formatted prompt string
    """
    return """
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

NO generic responses. Make it specific and valuable.
"""


def create_tag_quality_prompt() -> str:
    """
    Create validation prompt for coherent tag generation.
    
    Returns:
        Formatted prompt string
    """
    return """
Analyze this news article and generate 3-5 COHERENT, SPECIFIC hashtags that:
1. Accurately reflect the article's main topics
2. Are relevant to African audiences
3. Include specific countries/regions mentioned
4. Capture key themes (economy, technology, sustainability, mining, etc.)
5. Use proper capitalization (CamelCase)
6. Focus on the most important and specific aspects

CRITICAL: Tags must be coherent with the article content. Do NOT use generic tags.
PRIORITIZE: Most specific and relevant tags over generic ones.

Example outputs:
- For mining news: ["#ZambiaMining", "#CriticalMinerals", "#SupplyChainDiversification", "#USChinaRivalry"]
- For renewable energy: ["#GreenHydrogen", "#SouthAfrica", "#RenewableEnergy", "#CleanEnergy"]
- For tech news: ["#Nigeria", "#TechStartups", "#FinTech", "#AfricanInnovation"]
- For agriculture: ["#Kenya", "#AgriTech", "#FoodSecurity", "#SustainableFarming"]
"""
