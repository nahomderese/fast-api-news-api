# SWEN AI-Enriched News Pipeline

A production-ready, cloud-portable AI news enrichment service built with FastAPI and Clean Architecture principles. This service ingests raw news articles and enriches them with AI-generated metadata, summaries, tags, relevance scores, media URLs, and contextual information using OpenAI ChatGPT.


## 🔗 Live Demo

🌐 **Live API**: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/)

- API Documentation: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/docs](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/docs)
- ReDoc: [https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/redoc](https://swen-api.delightfulstone-4258e88a.westus2.azurecontainerapps.io/redoc)

---

## 🧩 SWEN Architecture Implementation

This implementation directly reflects **SWEN's architectural principles** through:

- **🎯 Domain-Driven Design**: Clear separation between news ingestion, AI enrichment, and data persistence domains
- **🔄 Event-Driven Architecture**: Asynchronous processing pipeline with clear event boundaries (ingest → enrich → store)
- **📊 Data Pipeline Architecture**: Multi-stage processing with validation, transformation, and enrichment stages
- **🌐 Microservices-Ready**: Containerized, stateless services with externalized configuration
- **🔌 API-First Design**: RESTful endpoints with comprehensive OpenAPI documentation
- **📈 Scalable Processing**: Queue-based architecture ready for horizontal scaling

## 🏗️ Technical Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
swen_ai_pipeline/
├── api/v1/endpoints.py      # API layer - REST endpoints
├── services/                # Business logic layer
│   ├── ai_service.py        # AI/ML operations (OpenAI ChatGPT integration)
│   └── ingestion_service.py # Orchestration & workflow
├── db/repository.py         # Data access layer
├── models/data_models.py    # Pydantic models (contracts)
├── core/config.py           # Configuration management
└── main.py                  # Application entry point
```

### Key Design Principles

- **Separation of Concerns**: Each layer has a single, well-defined responsibility
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Testability**: Mock-friendly design with dependency injection
- **Cloud Portability**: Containerized with infrastructure-as-code for AWS and Alibaba Cloud

## 🚀 Features

### API Endpoints

1. **POST /api/v1/ingest** - Ingest and enrich news articles
   - Accepts raw news data (title, body, source URL, etc.)
   - Processes through AI enrichment pipeline
   - Returns fully enriched article with unique UUID

2. **GET /api/v1/news/{id}** - Retrieve full article by UUID
   - Returns complete enriched news article
   - Includes all AI-generated fields and metadata

3. **GET /api/v1/news** - List all articles
   - Paginated results (limit/offset)
   - Returns article summaries
   - Sorted by ingestion date

4. **GET /api/v1/health** - Health check
5. **GET /api/v1/stats** - Pipeline statistics

### ✨ SWEN Schema Compliance

The API now produces **exactly 17 fields** as per SWEN requirements:
- ✅ Strict field control with Pydantic aliases
- ✅ Automatic null value exclusion
- ✅ UUID-based identification
- ✅ Flexible input: accepts both `author`/`published_date` AND `publisher`/`published_at`
- ✅ Consistent output: always uses `publisher` and `published_at` field names

### AI Enrichment Features

The AI service generates **high-quality, non-placeholder content**:
- ✅ **Unique UUID** - Auto-generated identifier
- ✅ **Summary** - AI-generated article summary (African focus)
- ✅ **Coherent Tags** - Specific hashtags reflecting actual content
- ✅ **Relevance Score** - 0.0 to 1.0 quality metric
- ✅ **Real Media URLs** - Working Unsplash images & YouTube videos (NO placeholders)
- ✅ **Media Justification** - Detailed explanation of media selection
- ✅ **Rich Wikipedia Snippet** - 50-100 words of contextual background
- ✅ **Social Sentiment** - Positive/negative/neutral (African perspective)
- ✅ **Search Trend** - Rising/stable/declining/viral
- ✅ **Accurate Geo Coordinates** - Precise lat/lng for mentioned locations
- ✅ **Google Maps URL** - Direct link to location

### 🌟 Content Quality Highlights

**No More Placeholders!**
- Tags are **coherent and specific** (e.g., "#Nigeria #FinTech #PayStack" not just "#Africa #News")
- Media URLs are **real and working** (real Unsplash photo IDs, real YouTube video IDs)
- Geo coordinates are **accurate** (extracted from article content with validation)
- Context is **rich and detailed** (50-100 words of insightful background)

## 🎥 Media URL Verification

**✅ Confirmed: All media URLs are REAL and RELEVANT**

- **🖼️ Featured Images**: Discovered using **Brave Search API** for intelligent, context-aware image discovery
- **🎬 Related Videos**: Real video URLs sourced from authoritative content providers via Brave Search
- **🔍 Content Relevance**: AI generates targeted search queries, then Brave Search finds contextually appropriate media
- **🌍 Geographic Accuracy**: Images and videos match the geographic context mentioned in articles
- **📊 Quality Validation**: All URLs are tested for accessibility and relevance before inclusion
- **🚀 Smart Discovery**: Brave Search API provides real-time access to current, relevant media from across the web

**No placeholder URLs like "https://example.com/image.jpg" are used in production. All media is discovered through intelligent search.**

## 📦 Installation

### Prerequisites

- [mise](https://mise.jdx.dev/) - Tool version manager
- Docker and Docker Compose (for containerized development)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SWEN-backend-test
   ```

2. **Install mise and setup environment**
   ```bash
   # Install mise (if not already installed)
   curl https://mise.jdx.dev/install.sh | sh
   
   # Install Python and dependencies
   mise install
   ```

3. **Verify setup**
   ```bash
   mise doctor
   ```

## 🏃 Running the Application

### Local Development

```bash
# Start development server (uses mise configuration)
mise run dev

# Or use the Makefile
make dev
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Using Docker Compose

```bash
# Start all services (API + PostgreSQL) via mise
mise run docker

# Or use the Makefile
make docker

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Database Setup

```bash
# Initialize database
mise run db-init

# Or use the Makefile
make db-init
```

The Docker Compose setup includes:
- **API Service**: FastAPI application on port 8000
- **PostgreSQL Database**: Database service on port 5432
- **Automatic Health Checks**: Services wait for dependencies
- **Volume Mounting**: Live code reloading for development

## 📝 Usage Examples

### Ingest a News Article

```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "South Africa set to open first underground gold mine in 15 years",
    "body": "South Africa is set to open its first new underground gold mine in 15 years...",
    "source_url": "https://www.mining.com/web/south-africa-gold-mine/",
    "publisher": "Mining.com",
    "published_at": "2025-08-21T07:03:00Z"
  }'

# Alternative format (both work):
# "author": "Mining.com",
# "published_date": "2025-08-21T07:03:00Z"
```

### Get Article by Slug

```bash
curl "http://localhost:8000/api/v1/news/breaking-ai-revolutionizes-news-industry-abc12345"
```

### List All Articles

```bash
curl "http://localhost:8000/api/v1/news?limit=10&offset=0"
```

## 🤖 AI Tools & Development Acceleration

### Google Gemini Integration & AI-Powered Development

This project leverages **multiple AI tools** to accelerate development and enhance functionality:

#### 🧠 **Google Gemini Integration**
- **Primary AI Engine**: Used for content analysis and enrichment (Gemini 2.5 Flash)
- **Multi-language Support**: Handles African news content in various languages
- **Context Understanding**: Deep comprehension of African political, economic, and social contexts
- **Real-time Processing**: Fast inference for production workloads
- **Note**: Originally planned to use Qwen (Alibaba Cloud AI), but switched to Google Gemini due to API access limitations

#### 🔍 **Brave Search API Integration**
- **Smart Media Discovery**: Uses Brave Search API for intelligent image and video URL discovery
- **Context-Aware Search**: AI generates targeted search queries based on article content
- **Real Media Sources**: Discovers actual images and videos from authoritative content providers
- **Quality Assurance**: Validates media URLs for accessibility and relevance
- **Fallback Strategy**: Gracefully handles API failures with appropriate error handling

#### 🚀 **Development Acceleration Examples**

1. **Code Generation & Optimization**
   - AI-assisted FastAPI endpoint generation
   - Automated Pydantic model creation with proper validation
   - Smart error handling patterns

2. **Architecture Design**
   - AI-guided Clean Architecture implementation
   - Dependency injection pattern suggestions
   - Database schema optimization recommendations

3. **Content Processing**
   - Intelligent tag extraction using NLP
   - Automated summary generation with African context
   - Smart media selection based on content analysis

4. **Testing & Quality Assurance**
   - AI-generated test cases for edge scenarios
   - Automated API documentation generation
   - Performance optimization suggestions

#### 🛠️ **AI Tools Used in Development**
- **GitHub Copilot**: Real-time code completion and suggestions
- **ChatGPT/Claude**: Architecture design and problem-solving
- **Google Gemini API**: Content analysis and enrichment (Gemini 2.5 Flash)
- **Brave Search API**: Smart media discovery for relevant images and videos
- **AI Code Review**: Automated code quality checks

## 🧪 Testing

```bash
# Run tests via mise
mise run test

# Or use the Makefile
make test
```

The service includes a mock AI implementation for testing and development. The configuration is managed through `mise.toml`:

### AI Service Configuration

The project uses Google Gemini API for AI enrichment. Configuration is handled in `mise.toml`:

```toml
[env]
USE_MOCK_AI = "false"
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-2.5-flash"
```

To use mock AI for development, set `USE_MOCK_AI = "true"` in `mise.toml`.

## 🌐 Cloud Deployment

### AWS Deployment (EKS)

Infrastructure-as-Code for AWS is available in `iac/aws/`:

```bash
cd iac/aws
terraform init
terraform plan
terraform apply
```

### Alibaba Cloud Deployment (ACK)

Infrastructure-as-Code for Alibaba Cloud is available in `iac/alibaba_cloud/`:

```bash
cd iac/alibaba_cloud
terraform init
terraform plan
terraform apply
```

## 🔧 Configuration

Configuration is managed through `mise.toml`. All environment variables are defined in the `[env]` section:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | SWEN AI-Enriched News Pipeline |
| `ENVIRONMENT` | Environment (dev/staging/prod) | development |
| `HOST` | API host | 0.0.0.0 |
| `PORT` | API port | 8000 |
| `USE_MOCK_AI` | Use mock AI service | false |
| `GEMINI_API_KEY` | Google Gemini API key | Configured in mise.toml |
| `GEMINI_MODEL` | Gemini model to use | gemini-2.5-flash |
| `DATABASE_URL` | Database connection URL | Configured in mise.toml |
| `DB_HOST` | Database host | postgres |
| `DB_PORT` | Database port | 5432 |
| `DB_NAME` | Database name | swen_news |
| `DB_USER` | Database user | swen_user |
| `DB_PASSWORD` | Database password | Configured in mise.toml |

### Available Tasks

The project includes several predefined tasks in `mise.toml`:

- `mise run dev` - Start development server
- `mise run docker` - Start services with docker-compose
- `mise run db-init` - Initialize database
- `mise run test` - Run tests

### Docker Compose Environment

When using Docker Compose, all environment variables are automatically configured from `mise.toml`:
- Database connection is set up automatically between services
- Volume mounting enables live code reloading
- Health checks ensure proper service startup order

## 📊 Data Models

### Input Model: RawNewsInput
```json
{
  "title": "string",
  "body": "string",
  "source_url": "https://example.com",
  "author": "string (optional)",
  "published_date": "string (optional)"
}
```

### Output Model: FinalNewsOutput
```json
{
  "slug": "unique-article-identifier",
  "title": "string",
  "body": "string",
  "source_url": "https://example.com",
  "author": "string",
  "published_date": "string",
  "summary": "AI-generated summary",
  "tags": ["tag1", "tag2"],
  "relevance_score": 0.85,
  "media": {
    "featured_image_url": "https://...",
    "related_video_url": "https://...",
    "thumbnail_url": "https://..."
  },
  "context": {
    "wikipedia_snippet": "...",
    "social_sentiment": "positive",
    "related_topics": ["topic1", "topic2"],
    "geographic_locations": ["location1"],
    "key_entities": ["entity1", "entity2"]
  },
  "ingested_at": "2025-10-16T12:00:00",
  "processed_at": "2025-10-16T12:00:01"
}
```

## 🏛️ Clean Architecture Layers

### 1. API Layer (`api/v1/endpoints.py`)
- Handles HTTP requests/responses
- Input validation via Pydantic
- No business logic

### 2. Service Layer (`services/`)
- **AI Service**: All AI/ML operations
  - OpenAI ChatGPT integration
  - Summary generation
  - Tag extraction
  - Media discovery
  - Context analysis
- **Ingestion Service**: Orchestration
  - Pipeline workflow
  - Error handling
  - Transaction management

### 3. Repository Layer (`db/repository.py`)
- Data access abstraction
- Currently: In-memory storage
- Future: Database integration (PostgreSQL, MongoDB)

### 4. Models Layer (`models/data_models.py`)
- Pydantic models
- Data contracts
- Validation rules

## 🔐 Security Considerations

- [ ] API key authentication for production
- [ ] Rate limiting
- [x] Input sanitization
- [ ] CORS configuration
- [ ] HTTPS/TLS in production

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed as part of the SWEN technical assessment.


**Note**: This implementation uses Google Gemini API for AI enrichment. Configuration is managed through `mise.toml`. To use mock AI for development, set `USE_MOCK_AI=true` in the `[env]` section of `mise.toml`.

