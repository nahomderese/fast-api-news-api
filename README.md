# SWEN AI-Enriched News Pipeline

A production-ready AI news enrichment service that ingests raw news articles and enriches them with AI-generated metadata, summaries, tags, relevance scores, and contextual information.

## 🔗 Live Demo

🌐 **Live API**: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/)

- API Documentation: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/docs](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/docs)
- ReDoc: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/redoc](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/redoc)

---

## 🧩 SWEN Architecture Implementation

This implementation reflects **SWEN's architectural principles** through:
- **🎯 Domain-Driven Design**: Clear separation between news ingestion, AI enrichment, and data persistence
- **🔄 Event-Driven Architecture**: Asynchronous processing pipeline with clear event boundaries
- **📊 Data Pipeline Architecture**: Multi-stage processing with validation, transformation, and enrichment
- **🌐 Microservices-Ready**: Containerized, stateless services with externalized configuration
- **🔌 API-First Design**: RESTful endpoints with comprehensive OpenAPI documentation

## 🚀 Key Features

### API Endpoints
- **POST /api/v1/ingest** - Ingest and enrich news articles
- **GET /api/v1/news/{id}** - Retrieve full article by UUID
- **GET /api/v1/news** - List all articles (paginated)
- **GET /api/v1/health** - Health check
- **GET /api/v1/stats** - Pipeline statistics

### ✨ SWEN Schema Compliance
- ✅ **Exactly 17 fields** as per SWEN requirements
- ✅ Strict field control with Pydantic aliases
- ✅ UUID-based identification
- ✅ Flexible input: accepts both `author`/`published_date` AND `publisher`/`published_at`
- ✅ Consistent output: always uses `publisher` and `published_at` field names

### AI Enrichment Features
- ✅ **Unique UUID** - Auto-generated identifier
- ✅ **Summary** - AI-generated article summary (African focus)
- ✅ **Coherent Tags** - Specific hashtags reflecting actual content
- ✅ **Relevance Score** - 0.0 to 1.0 quality metric
- ✅ **Real Media URLs** - Working images & videos (NO placeholders)
- ✅ **Rich Wikipedia Snippet** - 50-100 words of contextual background
- ✅ **Social Sentiment** - Positive/negative/neutral (African perspective)
- ✅ **Accurate Geo Coordinates** - Precise lat/lng for mentioned locations

## 🎥 Media URL Verification

**✅ All media URLs are REAL and RELEVANT**

- **🖼️ Featured Images**: Discovered using **Brave Search API** for intelligent, context-aware image discovery
- **🎬 Related Videos**: Real video URLs sourced from authoritative content providers via Brave Search
- **🔍 Content Relevance**: AI generates targeted search queries, then Brave Search finds contextually appropriate media
- **🚀 Smart Discovery**: Real-time access to current, relevant media from across the web

**No placeholder URLs are used in production. All media is discovered through intelligent search.**

## 🤖 AI Tools & Development Acceleration

### Google Gemini Integration
- **Primary AI Engine**: Content analysis and enrichment (Gemini 2.5 Flash)
- **Multi-language Support**: Handles African news content in various languages
- **Context Understanding**: Deep comprehension of African political, economic, and social contexts
- **Note**: Originally planned to use Qwen (Alibaba Cloud AI), but switched to Google Gemini due to API access limitations

### Brave Search API Integration
- **Smart Media Discovery**: Uses Brave Search API for intelligent image and video URL discovery
- **Context-Aware Search**: AI generates targeted search queries based on article content
- **Real Media Sources**: Discovers actual images and videos from authoritative content providers
- **Quality Assurance**: Validates media URLs for accessibility and relevance

### AI Tools Used in Development
- **GitHub Copilot**: Real-time code completion and suggestions
- **ChatGPT/Claude**: Architecture design and problem-solving
- **Google Gemini API**: Content analysis and enrichment (Gemini 2.5 Flash)
- **Brave Search API**: Smart media discovery for relevant images and videos

## 🏃 Quick Start

### Prerequisites
- [mise](https://mise.jdx.dev/) - Tool version manager
- Docker and Docker Compose

### Setup & Run
```bash
# Clone and setup
git clone <repository-url>
cd SWEN-backend-test
mise install

# Start development server
mise run dev

# Or use Docker
mise run docker
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs

### Example Usage
```bash
# Ingest a news article
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "South Africa set to open first underground gold mine in 15 years",
    "body": "South Africa is set to open its first new underground gold mine in 15 years...",
    "source_url": "https://www.mining.com/web/south-africa-gold-mine/",
    "publisher": "Mining.com",
    "published_at": "2025-08-21T07:03:00Z"
  }'
```

## 🧪 Testing
```bash
mise run test
```

## 🌐 Cloud Deployment

### Azure Container Apps (Current)
Deployed at: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/)

### Infrastructure-as-Code Available
- **AWS**: `iac/aws/` (Terraform)
- **Alibaba Cloud**: `iac/alibaba_cloud/` (Terraform)

## 🔧 Configuration

Configuration is managed through `mise.toml`:

```toml
[env]
USE_MOCK_AI = "false"
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-2.5-flash"
BRAVE_API_KEY = "your-brave-api-key"
```

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed as part of the SWEN technical assessment.

---

**Note**: This implementation uses Google Gemini API for AI enrichment and Brave Search API for media discovery. Configuration is managed through `mise.toml`.