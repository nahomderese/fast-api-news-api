
```bash
├── swen_ai_pipeline/
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints.py      # Defines all API routes: POST /ingest, GET /news, GET /news/{slug}
│   │   └── __init__.py
│   ├── core/
│   │   └── config.py             # Loads settings (Qwen API Key, environment, etc.)
│   ├── db/
│   │   └── repository.py         # Handles data access (Saving and Fetching news items)
│   ├── models/
│   │   ├── data_models.py        # Pydantic models for ALL JSON structures (Input, List, Output)
│   │   └── __init__.py
│   ├── services/
│   │   ├── ai_service.py         # Primary AI logic (Calls Qwen, handles media search)
│   │   ├── ingestion_service.py  # Orchestrates the AI pipeline flow
│   │   └── __init__.py
│   └── main.py                   # FastAPI application entry point
├── iac/
│   ├── aws/
│   │   └── main.tf               # Terraform config for AWS resources
│   └── alibaba_cloud/
│       └── main.tf               # Terraform config for Alibaba Cloud
├── Dockerfile                    # Container build specs
└── README.md                     # Project documentation and live link
```