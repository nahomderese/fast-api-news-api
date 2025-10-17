# Key Structural Components Explained

This structure directly maps to the SWEN architecture and addresses the test requirements.

## Environment Management

This project uses [mise](https://mise.jdx.dev/) for environment management and tool versioning:

- **`.mise.toml`** - Contains all environment variables, Python version, and predefined tasks
- **No `.env` files needed** - All configuration is centralized in mise.toml
- **Consistent environment** - Same configuration across development, testing, and deployment

## 1. `swen_ai_pipeline/models/data_models.py` (The Contract)

This is the most crucial file. **Define all data structures using Pydantic** here:

- **RawNewsInput:**  
  Defines the required input fields (e.g., `title`, `body`, `source_url`, etc.).

- **EnrichedNewsMedia:**  
  Defines the nested media object (fields like `featured_image_url`, `related_video_url`, etc.).

- **EnrichedNewsContext:**  
  Defines the nested context object (fields such as `wikipedia_snippet`, `social_sentiment`, etc.).

- **FinalNewsOutput:**  
  Represents the complete, single JSON output object required by the API.

---

## 2. `swen_ai_pipeline/services/` (The Brain)

This directory contains the business logic implementing SWEN's "AI Transformation".

- **`ai_service.py`** serves as the Artificial Intelligence Services container.
  - Calls the Qwen LLM (or a mock in development).
  - Generates core AI fields: *Summary*, *Tags*, *Relevance Score*.
  - Handles complex contextual intelligence fields.
  - Contains the logic for media search based on LLM output to fulfill `featured_image_url` and `related_video_url` requirements.

---

## 3. `swen_ai_pipeline/api/v1/endpoints.py` (The API)

Handles external request/response cycles:

- Implements the `GET /api/v1/news/{id}` endpoint.
- Uses `repository.py` to fetch the final, stored JSON object.

---

## 4. `iac/` (The Infrastructure)

Addresses the requirement for cloud portability:

- Contains two separate directories, each with its own Terraform code.
  - One for AWS (EKS).
  - One for Alibaba Cloud (ACK).
- Demonstrates that the architecture is cloud portable.

---
