"""
Constants and configuration for AI service operations.
"""
from typing import Dict, List, Tuple

# African cities coordinates database
AFRICAN_CITIES_COORDINATES: Dict[str, Tuple[float, float]] = {
    "Nairobi": (-1.286389, 36.817223),
    "Lagos": (6.5244, 3.3792),
    "Johannesburg": (-26.2041, 28.0473),
    "Cairo": (30.0444, 31.2357),
    "Addis Ababa": (9.0320, 38.7469),
    "Accra": (5.6037, -0.1870),
    "Dar es Salaam": (-6.7924, 39.2083),
    "Kigali": (-1.9536, 30.0606),
    "Casablanca": (33.5731, -7.5898),
    "Tunis": (36.8065, 10.1815),
    "Algiers": (36.7538, 3.0588),
    "Khartoum": (15.5007, 32.5599),
    "Kampala": (0.3476, 32.5825),
    "Abuja": (9.0765, 7.3986),
    "Dakar": (14.6928, -17.4467),
    "Bamako": (12.6392, -8.0029),
    "Ouagadougou": (12.3714, -1.5197),
    "Niamey": (13.5137, 2.1098),
    "Yaounde": (3.8480, 11.5021),
    "Kinshasa": (-4.4419, 15.2663),
    "Brazzaville": (-4.2634, 15.2429),
    "Luanda": (-8.8390, 13.2894),
    "Lusaka": (-15.3875, 28.3228),
    "Harare": (-17.8292, 31.0522),
    "Gaborone": (-24.6282, 25.9231),
    "Windhoek": (-22.5609, 17.0658),
    "Cape Town": (-33.9249, 18.4241),
    "Durban": (-29.8587, 31.0218),
    "Port Elizabeth": (-33.9608, 25.6022),
    "Bloemfontein": (-29.0852, 26.1596),
    "Pretoria": (-25.7479, 28.2293),
    "Maputo": (-25.9692, 32.5732),
    "Antananarivo": (-18.8792, 47.5079),
    "Victoria": (-4.6200, 55.4500),
    "Port Louis": (-20.1619, 57.4989),
    "Moroni": (-11.7172, 43.2473),
    "Djibouti": (11.8251, 42.5903),
    "Asmara": (15.3229, 38.9251),
    "Mogadishu": (2.0469, 45.3182),
    "Juba": (4.8594, 31.5713),
    "Bangui": (4.3947, 18.5582),
    "N'Djamena": (12.1348, 15.0557),
    "Libreville": (0.4162, 9.4673),
    "Malabo": (3.7504, 8.7371),
    "São Tomé": (0.1864, 6.6131),
    "Banjul": (13.4432, -16.5819),
    "Bissau": (11.8037, -15.1804),
    "Conakry": (9.6412, -13.5784),
    "Freetown": (8.4840, -13.2299),
    "Monrovia": (6.3008, -10.7970),
    "Abidjan": (5.3600, -4.0083),
    "Yamoussoukro": (6.8276, -5.2893),
    "Lomé": (6.1725, 1.2314),
    "Cotonou": (6.3725, 2.3544),
    "Porto-Novo": (6.4969, 2.6289),
    "Lagos": (6.5244, 3.3792),
    "Abuja": (9.0765, 7.3986),
    "Douala": (4.0483, 9.7043),
    "Yaounde": (3.8480, 11.5021),
    "Bangui": (4.3947, 18.5582),
    "N'Djamena": (12.1348, 15.0557),
    "Khartoum": (15.5007, 32.5599),
    "Juba": (4.8594, 31.5713),
    "Addis Ababa": (9.0320, 38.7469),
    "Asmara": (15.3229, 38.9251),
    "Djibouti": (11.8251, 42.5903),
    "Mogadishu": (2.0469, 45.3182),
    "Nairobi": (-1.286389, 36.817223),
    "Kampala": (0.3476, 32.5825),
    "Kigali": (-1.9536, 30.0606),
    "Bujumbura": (-3.3614, 29.3599),
    "Dar es Salaam": (-6.7924, 39.2083),
    "Dodoma": (-6.1630, 35.7516),
    "Lusaka": (-15.3875, 28.3228),
    "Harare": (-17.8292, 31.0522),
    "Gaborone": (-24.6282, 25.9231),
    "Windhoek": (-22.5609, 17.0658),
    "Cape Town": (-33.9249, 18.4241),
    "Johannesburg": (-26.2041, 28.0473),
    "Durban": (-29.8587, 31.0218),
    "Bloemfontein": (-29.0852, 26.1596),
    "Pretoria": (-25.7479, 28.2293),
    "Maseru": (-29.3167, 27.4833),
    "Mbabane": (-26.3054, 31.1367),
    "Maputo": (-25.9692, 32.5732),
    "Antananarivo": (-18.8792, 47.5079),
    "Victoria": (-4.6200, 55.4500),
    "Port Louis": (-20.1619, 57.4989),
    "Moroni": (-11.7172, 43.2473),
    "Cairo": (30.0444, 31.2357),
    "Alexandria": (31.2001, 29.9187),
    "Tripoli": (32.8872, 13.1913),
    "Tunis": (36.8065, 10.1815),
    "Algiers": (36.7538, 3.0588),
    "Rabat": (34.0209, -6.8416),
    "Casablanca": (33.5731, -7.5898),
    "Fez": (34.0181, -5.0078),
    "Marrakech": (31.6295, -7.9811),
    "Nouakchott": (18.0735, -15.9582),
    "Bamako": (12.6392, -8.0029),
    "Ouagadougou": (12.3714, -1.5197),
    "Niamey": (13.5137, 2.1098),
    "Abuja": (9.0765, 7.3986),
    "Lagos": (6.5244, 3.3792),
    "Kano": (12.0022, 8.5920),
    "Ibadan": (7.3776, 3.9470),
    "Benin City": (6.3350, 5.6037),
    "Port Harcourt": (4.8156, 7.0498),
    "Kaduna": (10.5200, 7.4382),
    "Maiduguri": (11.8333, 13.1500),
    "Zaria": (11.0667, 7.7000),
    "Aba": (5.1167, 7.3667),
    "Jos": (9.9167, 8.9000),
    "Ilorin": (8.5000, 4.5500),
    "Oyo": (7.8500, 3.9333),
    "Enugu": (6.4500, 7.5000),
    "Abeokuta": (7.1500, 3.3500),
    "Sokoto": (13.0667, 5.2333),
    "Onitsha": (6.1667, 6.7833),
    "Warri": (5.5167, 5.7500),
    "Kaduna": (10.5200, 7.4382),
    "Maiduguri": (11.8333, 13.1500),
    "Zaria": (11.0667, 7.7000),
    "Aba": (5.1167, 7.3667),
    "Jos": (9.9167, 8.9000),
    "Ilorin": (8.5000, 4.5500),
    "Oyo": (7.8500, 3.9333),
    "Enugu": (6.4500, 7.5000),
    "Abeokuta": (7.1500, 3.3500),
    "Sokoto": (13.0667, 5.2333),
    "Onitsha": (6.1667, 6.7833),
    "Warri": (5.5167, 5.7500)
}

# Default fallback URLs for media
DEFAULT_MEDIA_URLS = {
    "featured_image": "https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800&q=80",
    "related_video": "https://www.youtube.com/watch?v=zn8o_DwUwFk",
    "fallback_image": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800"
}

# Default fallback content
DEFAULT_FALLBACKS = {
    "tags": ["#Africa", "#News", "#Development"],
    "summary": "This article provides important insights relevant to African markets and development.",
    "wikipedia_snippet": "This article covers topics of significance to African audiences and regional development.",
    "social_sentiment": "neutral",
    "search_trend": "stable",
    "relevance_score": 0.7,
    "media_justification": "High-quality media content selected from authoritative sources for African audience engagement and understanding",
    "featured_image_url": "https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800&q=80",
    "image_caption": "High-quality image relevant to African development and sustainability",
    "related_video_url": "https://www.youtube.com/watch?v=zn8o_DwUwFk",
    "video_caption": "Authoritative video content on African development",
    "geo_lat": 0.0,
    "geo_lng": 20.0,
    "map_url": "https://www.google.com/maps?q=0.0,20.0"
}

# Content validation limits
CONTENT_LIMITS = {
    "min_snippet_length": 20,
    "max_tags": 5,
    "min_tags": 3,
    "min_justification_length": 50,
    "body_preview_length": 1500,
    "title_preview_length": 800
}

# Coordinate validation ranges
COORDINATE_RANGES = {
    "lat_min": -90.0,
    "lat_max": 90.0,
    "lng_min": -180.0,
    "lng_max": 180.0
}

# URL patterns for validation
URL_PATTERNS = {
    "unsplash_direct": "images.unsplash.com/photo-",
    "unsplash_source": "source.unsplash.com",
    "youtube_watch": "youtube.com/watch?v=",
    "youtube_search": "search_query",
    "youtube_results": "results"
}

# Common African themes for content generation
AFRICAN_THEMES = [
    "renewable energy", "sustainable development", "green technology",
    "fintech", "mobile money", "digital banking", "startups", "innovation",
    "agriculture", "food security", "climate change", "infrastructure",
    "education", "healthcare", "trade", "investment", "tourism",
    "culture", "art", "music", "sports", "youth", "women empowerment",
    "urbanization", "rural development", "mining", "oil and gas",
    "manufacturing", "textiles", "telecommunications", "transportation"
]

# Sentiment analysis options
SENTIMENT_OPTIONS = ["positive", "negative", "neutral"]

# Search trend options
TREND_OPTIONS = ["viral", "rising", "stable", "declining"]
