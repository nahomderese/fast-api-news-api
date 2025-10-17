"""
Brave Search API service for discovering media content (images and videos).
"""
import httpx
from typing import Optional, Dict, Any
from swen_ai_pipeline.core.config import settings


class BraveSearchService:
    """
    Service for interacting with Brave Search API to discover images and videos.
    """
    
    def __init__(self):
        """Initialize the Brave Search service with API credentials."""
        self.api_key = settings.brave_api_key
        self.image_search_url = settings.brave_image_search_url
        self.video_search_url = settings.brave_video_search_url
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key if self.api_key else ""
        }
    
    async def search_images(self, query: str, count: int = 1) -> Optional[Dict[str, Any]]:
        """
        Search for images using Brave Search API.
        
        Args:
            query: Search query string
            count: Number of results to return (default: 1)
            
        Returns:
            First image result with URL and metadata, or None if not found
            
        Response structure:
        {
          "results": [
            {
              "title": "Image title",
              "url": "https://page-url.com",  # Page URL
              "source": "domain.com",
              "thumbnail": {"src": "...", "width": 500, "height": 500},
              "properties": {
                "url": "https://actual-image-url.jpg",  # Actual image URL
                "width": 500,
                "height": 500
              }
            }
          ]
        }
        """
        if not self.api_key:
            print("Warning: BRAVE_API_KEY not configured")
            return None
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.image_search_url,
                    headers=self.headers,
                    params={
                        "q": query,
                        "count": count,
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract first result
                if data.get("results") and len(data["results"]) > 0:
                    first_result = data["results"][0]
                    # The actual image URL is in properties.url
                    image_url = first_result.get("properties", {}).get("url")
                    
                    return {
                        "url": image_url,  # Actual image URL from properties
                        "page_url": first_result.get("url"),  # Page where image is found
                        "title": first_result.get("title"),
                        "source": first_result.get("source"),
                        "thumbnail": first_result.get("thumbnail", {}).get("src"),
                        "width": first_result.get("properties", {}).get("width"),
                        "height": first_result.get("properties", {}).get("height")
                    }
                return None
                
        except httpx.HTTPError as e:
            print(f"Brave Image Search API error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in image search: {e}")
            return None
    
    async def search_videos(self, query: str, count: int = 1) -> Optional[Dict[str, Any]]:
        """
        Search for videos using Brave Search API.
        
        Args:
            query: Search query string
            count: Number of results to return (default: 1)
            
        Returns:
            First video result with URL and metadata, or None if not found
        """
        if not self.api_key:
            print("Warning: BRAVE_API_KEY not configured")
            return None
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.video_search_url,
                    headers=self.headers,
                    params={
                        "q": query,
                        "count": count,
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract first result
                if data.get("results") and len(data["results"]) > 0:
                    first_result = data["results"][0]
                    return {
                        "url": first_result.get("url"),
                        "title": first_result.get("title"),
                        "description": first_result.get("description"),
                        "thumbnail": first_result.get("thumbnail", {}).get("src"),
                        "duration": first_result.get("meta_url", {}).get("duration")
                    }
                return None
                
        except httpx.HTTPError as e:
            print(f"Brave Video Search API error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in video search: {e}")
            return None
    
    async def discover_media(self, query: str) -> Dict[str, Any]:
        """
        Discover both image and video media using a single search query.
        
        Args:
            query: Search query string generated by AI
            
        Returns:
            Dictionary containing query, image_url, and video_url
        """
        # Search for both images and videos in parallel (with country-specific results)
        image_result = await self.search_images(query)
        video_result = await self.search_videos(query)
        
        return {
            "query": query,
            "image_url": image_result.get("url") if image_result else None,
            "image_metadata": image_result,
            "video_url": video_result.get("url") if video_result else None,
            "video_metadata": video_result
        }


# Global instance
brave_search_service = BraveSearchService()

