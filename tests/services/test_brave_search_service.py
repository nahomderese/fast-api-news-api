"""
Tests for BraveSearchService.

This module contains comprehensive tests for the BraveSearchService class,
including tests for search_images and search_videos methods.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from typing import Dict, Any

from swen_ai_pipeline.services.brave_search_service import BraveSearchService


class TestBraveSearchService:
    """Test cases for BraveSearchService."""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings for testing."""
        with patch('swen_ai_pipeline.services.brave_search_service.settings') as mock:
            mock.brave_api_key = "BSArZUnBKyazQ6pk7h6npB3fbzYw_y9"
            mock.brave_image_search_url = "https://api.search.brave.com/res/v1/images/search"
            mock.brave_video_search_url = "https://api.search.brave.com/res/v1/videos/search"
            yield mock

    @pytest.fixture
    def service(self, mock_settings):
        """Create a BraveSearchService instance for testing."""
        return BraveSearchService()

    @pytest.fixture
    def mock_image_response(self):
        """Mock successful image search response."""
        return {
            "results": [
                {
                    "title": "Test Image",
                    "url": "https://example.com/page",
                    "source": "example.com",
                    "thumbnail": {
                        "src": "https://example.com/thumb.jpg",
                        "width": 200,
                        "height": 200
                    },
                    "properties": {
                        "url": "https://example.com/image.jpg",
                        "width": 800,
                        "height": 600
                    }
                }
            ]
        }

    @pytest.fixture
    def mock_video_response(self):
        """Mock successful video search response."""
        return {
            "results": [
                {
                    "url": "https://example.com/video",
                    "title": "Test Video",
                    "description": "A test video description",
                    "thumbnail": {
                        "src": "https://example.com/video_thumb.jpg"
                    },
                    "meta_url": {
                        "duration": "2:30"
                    }
                }
            ]
        }

    # Tests for search_images method

    @pytest.mark.asyncio
    async def test_search_images_success(self, service, mock_image_response):
        """Test successful image search."""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock the async context manager
            mock_response = MagicMock()
            mock_response.json.return_value = mock_image_response
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_images("test query")

            assert result is not None
            assert result["url"] == "https://example.com/image.jpg"
            assert result["page_url"] == "https://example.com/page"
            assert result["title"] == "Test Image"
            assert result["source"] == "example.com"
            assert result["thumbnail"] == "https://example.com/thumb.jpg"
            assert result["width"] == 800
            assert result["height"] == 600

    @pytest.mark.asyncio
    async def test_search_images_with_custom_params(self, service, mock_image_response):
        """Test image search with custom parameters."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_image_response
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_images("test query", count=5, country="uk")

            # Verify the request was made with correct parameters
            mock_client_instance.get.assert_called_once()
            call_args = mock_client_instance.get.call_args
            assert call_args[1]["params"]["q"] == "test query"
            assert call_args[1]["params"]["count"] == 5
            assert call_args[1]["params"]["country"] == "uk"
            assert call_args[1]["params"]["search_lang"] == "en"
            assert call_args[1]["params"]["spellcheck"] == 1
            assert call_args[1]["params"]["safesearch"] == "moderate"

    @pytest.mark.asyncio
    async def test_search_images_no_results(self, service):
        """Test image search with no results."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {"results": []}
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_images("test query")

            assert result is None

    @pytest.mark.asyncio
    async def test_search_images_missing_properties(self, service):
        """Test image search with missing properties in response."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "results": [
                    {
                        "title": "Test Image",
                        "url": "https://example.com/page",
                        "source": "example.com"
                        # Missing properties and thumbnail
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_images("test query")

            assert result is not None
            assert result["url"] is None  # No properties.url
            assert result["page_url"] == "https://example.com/page"
            assert result["title"] == "Test Image"
            assert result["source"] == "example.com"
            assert result["thumbnail"] is None
            assert result["width"] is None
            assert result["height"] is None

    @pytest.mark.asyncio
    async def test_search_images_http_error(self, service):
        """Test image search with HTTP error."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = httpx.HTTPError("API Error")
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_images("test query")

            assert result is None

    @pytest.mark.asyncio
    async def test_search_images_general_exception(self, service):
        """Test image search with general exception."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = Exception("Unexpected error")
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_images("test query")

            assert result is None

    @pytest.mark.asyncio
    async def test_search_images_no_api_key(self):
        """Test image search without API key."""
        with patch('swen_ai_pipeline.services.brave_search_service.settings') as mock:
            mock.brave_api_key = None
            mock.brave_image_search_url = "https://api.search.brave.com/res/v1/images/search"
            mock.brave_video_search_url = "https://api.search.brave.com/res/v1/videos/search"
            
            service = BraveSearchService()
            result = await service.search_images("test query")

            assert result is None

    # Tests for search_videos method

    @pytest.mark.asyncio
    async def test_search_videos_success(self, service, mock_video_response):
        """Test successful video search."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_video_response
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_videos("test query")

            assert result is not None
            assert result["url"] == "https://example.com/video"
            assert result["title"] == "Test Video"
            assert result["description"] == "A test video description"
            assert result["thumbnail"] == "https://example.com/video_thumb.jpg"
            assert result["duration"] == "2:30"

    @pytest.mark.asyncio
    async def test_search_videos_with_custom_params(self, service, mock_video_response):
        """Test video search with custom parameters."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_video_response
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_videos("test query", count=3, country="ca")

            # Verify the request was made with correct parameters
            mock_client_instance.get.assert_called_once()
            call_args = mock_client_instance.get.call_args
            assert call_args[1]["params"]["q"] == "test query"
            assert call_args[1]["params"]["count"] == 3
            assert call_args[1]["params"]["country"] == "ca"
            assert call_args[1]["params"]["search_lang"] == "en"
            assert call_args[1]["params"]["spellcheck"] == 1
            assert call_args[1]["params"]["safesearch"] == "moderate"

    @pytest.mark.asyncio
    async def test_search_videos_no_results(self, service):
        """Test video search with no results."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {"results": []}
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_videos("test query")

            assert result is None

    @pytest.mark.asyncio
    async def test_search_videos_missing_fields(self, service):
        """Test video search with missing fields in response."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "results": [
                    {
                        "url": "https://example.com/video"
                        # Missing other fields
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_videos("test query")

            assert result is not None
            assert result["url"] == "https://example.com/video"
            assert result["title"] is None
            assert result["description"] is None
            assert result["thumbnail"] is None
            assert result["duration"] is None

    @pytest.mark.asyncio
    async def test_search_videos_http_error(self, service):
        """Test video search with HTTP error."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = httpx.HTTPError("API Error")
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_videos("test query")

            assert result is None

    @pytest.mark.asyncio
    async def test_search_videos_general_exception(self, service):
        """Test video search with general exception."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = Exception("Unexpected error")
            mock_client.return_value.__aenter__.return_value = mock_client_instance

            result = await service.search_videos("test query")

            assert result is None

    @pytest.mark.asyncio
    async def test_search_videos_no_api_key(self):
        """Test video search without API key."""
        with patch('swen_ai_pipeline.services.brave_search_service.settings') as mock:
            mock.brave_api_key = None
            mock.brave_image_search_url = "https://api.search.brave.com/res/v1/images/search"
            mock.brave_video_search_url = "https://api.search.brave.com/res/v1/videos/search"
            
            service = BraveSearchService()
            result = await service.search_videos("test query")

            assert result is None

    # Tests for discover_media method

    @pytest.mark.asyncio
    async def test_discover_media_success(self, service, mock_image_response, mock_video_response):
        """Test successful media discovery."""
        with patch.object(service, 'search_images', return_value=mock_image_response["results"][0]) as mock_img, \
             patch.object(service, 'search_videos', return_value=mock_video_response["results"][0]) as mock_vid:

            result = await service.discover_media("test query", country="us")

            assert result["query"] == "test query"
            assert result["image_url"] == "https://example.com/image.jpg"
            assert result["video_url"] == "https://example.com/video"
            assert result["image_metadata"] is not None
            assert result["video_metadata"] is not None

            mock_img.assert_called_once_with("test query", country="us")
            mock_vid.assert_called_once_with("test query", country="us")

    @pytest.mark.asyncio
    async def test_discover_media_no_results(self, service):
        """Test media discovery with no results."""
        with patch.object(service, 'search_images', return_value=None) as mock_img, \
             patch.object(service, 'search_videos', return_value=None) as mock_vid:

            result = await service.discover_media("test query")

            assert result["query"] == "test query"
            assert result["image_url"] is None
            assert result["video_url"] is None
            assert result["image_metadata"] is None
            assert result["video_metadata"] is None

    # Tests for service initialization

    def test_service_initialization(self, mock_settings):
        """Test service initialization with proper settings."""
        service = BraveSearchService()
        
        assert service.api_key == "test_api_key"
        assert service.image_search_url == "https://api.search.brave.com/res/v1/images/search"
        assert service.video_search_url == "https://api.search.brave.com/res/v1/videos/search"
        assert service.headers["X-Subscription-Token"] == "test_api_key"
        assert service.headers["Accept"] == "application/json"
        assert service.headers["Accept-Encoding"] == "gzip"

    def test_service_initialization_no_api_key(self):
        """Test service initialization without API key."""
        with patch('swen_ai_pipeline.services.brave_search_service.settings') as mock:
            mock.brave_api_key = None
            mock.brave_image_search_url = "https://api.search.brave.com/res/v1/images/search"
            mock.brave_video_search_url = "https://api.search.brave.com/res/v1/videos/search"
            
            service = BraveSearchService()
            
            assert service.api_key is None
            assert service.headers["X-Subscription-Token"] == ""

    # Integration-style tests (with real httpx but mocked responses)

    @pytest.mark.asyncio
    async def test_search_images_integration_style(self, service):
        """Test image search with mocked httpx response."""
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "results": [
                    {
                        "title": "Integration Test Image",
                        "url": "https://integration.com/page",
                        "source": "integration.com",
                        "thumbnail": {"src": "https://integration.com/thumb.jpg"},
                        "properties": {
                            "url": "https://integration.com/image.jpg",
                            "width": 1024,
                            "height": 768
                        }
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = await service.search_images("integration test")

            assert result is not None
            assert result["url"] == "https://integration.com/image.jpg"
            assert result["width"] == 1024
            assert result["height"] == 768

    @pytest.mark.asyncio
    async def test_search_videos_integration_style(self, service):
        """Test video search with mocked httpx response."""
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "results": [
                    {
                        "url": "https://integration.com/video",
                        "title": "Integration Test Video",
                        "description": "Integration test video description",
                        "thumbnail": {"src": "https://integration.com/video_thumb.jpg"},
                        "meta_url": {"duration": "5:45"}
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = await service.search_videos("integration test")

            assert result is not None
            assert result["url"] == "https://integration.com/video"
            assert result["title"] == "Integration Test Video"
            assert result["duration"] == "5:45"

    # Real API tests (no mocking)

    @pytest.mark.asyncio
    async def test_real_search_images(self):
        """Test real image search with Brave API."""
        
        with patch('swen_ai_pipeline.services.brave_search_service.settings') as mock:
            mock.brave_api_key = "BSArZUnBKyazQ6pk7h6npB3fbzYw_y9"
            mock.brave_image_search_url = "https://api.search.brave.com/res/v1/images/search"
            mock.brave_video_search_url = "https://api.search.brave.com/res/v1/videos/search"
            
        service = BraveSearchService()
        
        # Test with a real query
        query = "beautiful sunset landscape"
        print(f"\n🔍 Testing real image search with query: '{query}'")
        
        result = await service.search_images(query, count=1, country="us")
        
        if result is not None:
            print("✅ Image search successful!")
            print(f"📸 Image URL: {result.get('url')}")
            print(f"📄 Page URL: {result.get('page_url')}")
            print(f"🏷️  Title: {result.get('title')}")
            print(f"🌐 Source: {result.get('source')}")
            print(f"🖼️  Thumbnail: {result.get('thumbnail')}")
            print(f"📏 Dimensions: {result.get('width')}x{result.get('height')}")
        else:
            print("❌ Image search returned None")
            print("💡 Check if BRAVE_API_KEY is set in your environment")

    @pytest.mark.asyncio
    async def test_real_search_videos(self):
        """Test real video search with Brave API."""
        service = BraveSearchService()
        
        # Test with a real query
        query = "cooking tutorial pasta"
        print(f"\n🔍 Testing real video search with query: '{query}'")
        
        result = await service.search_videos(query, count=1, country="us")
        
        if result is not None:
            print("✅ Video search successful!")
            print(f"🎥 Video URL: {result.get('url')}")
            print(f"🏷️  Title: {result.get('title')}")
            print(f"📝 Description: {result.get('description')}")
            print(f"🖼️  Thumbnail: {result.get('thumbnail')}")
            print(f"⏱️  Duration: {result.get('duration')}")
        else:
            print("❌ Video search returned None")
            print("💡 Check if BRAVE_API_KEY is set in your environment")
