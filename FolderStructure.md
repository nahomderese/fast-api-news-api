
```bash
├── swen_ai_pipeline/             # Main application package
│   ├── api/                      # API layer
│   │   ├── v1/                   # API version 1
│   │   │   └── endpoints.py      # Defines all API routes: POST /ingest, GET /news, GET /news/{slug}
│   │   └── __init__.py
│   ├── core/                     # Core configuration
│   │   └── config.py             # Loads settings (API keys, environment, etc.)
│   ├── db/                       # Database layer
│   │   ├── database.py           # Database connection and session management
│   │   ├── models.py             # SQLAlchemy database models
│   │   └── repository.py         # Handles data access (Saving and Fetching news items)
│   ├── models/                   # Data models
│   │   ├── data_models.py        # Pydantic models for ALL JSON structures (Input, List, Output)
│   │   └── __init__.py
│   ├── services/                 # Business logic services
│   │   ├── ai_constants.py       # AI service constants and configurations
│   │   ├── ai_prompts.py         # AI prompt templates
│   │   ├── ai_service.py         # Primary AI logic (Calls Gemini, handles media search)
│   │   ├── ai_utils.py           # AI utility functions
│   │   ├── brave_search_service.py # Brave search API integration
│   │   ├── ingestion_service.py  # Orchestrates the AI pipeline flow
│   │   └── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   └── migrate_database.py       # Database migration script
├── tests/                        # Test suite
│   ├── services/                 # Service layer tests
│   │   └── test_brave_search_service.py # Brave search service tests
│   ├── __init__.py
│   └── README.md                 # Testing documentation
├── iac/                          # Infrastructure as Code
│   ├── aws/                      # AWS infrastructure
│   │   ├── main.tf               # Terraform config for AWS resources
│   │   ├── variables.tf          # AWS Terraform variables
│   │   └── README.md             # AWS deployment documentation
│   └── alibaba_cloud/            # Alibaba Cloud infrastructure
│       ├── main.tf               # Terraform config for Alibaba Cloud
│       ├── variables.tf          # Alibaba Cloud Terraform variables
│       └── README.md             # Alibaba Cloud deployment documentation
├── k8s/                          # Kubernetes deployment files
│   ├── configmap.yaml            # Kubernetes ConfigMap
│   ├── deployment.yaml           # Main application deployment
│   ├── ingress.yaml              # Ingress configuration
│   ├── postgres-deployment.yaml  # PostgreSQL deployment
│   ├── sealed-secret.yaml        # Sealed secrets configuration
│   ├── secret.yaml.example       # Example secret configuration
│   └── README.md                 # Kubernetes deployment documentation
├── Dockerfile                    # Container build specifications
├── docker-compose.yml            # Development environment setup
├── docker-compose.deploy.yml     # Production deployment configuration
├── env.template                  # Environment variables template
├── requirements.txt              # Python dependencies
├── pytest.ini                   # Pytest configuration
├── Makefile                      # Build and deployment commands
├── FolderStructure.md            # This file - project structure documentation
└── README.md                     # Project documentation and live link
```