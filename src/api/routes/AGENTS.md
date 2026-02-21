# `/src/api/routes` AGENTS.md

## Context

Holds controllers for specific API resources.

## Modules

- `ingest.py` - Contains the `/api/v1/ingest/...` endpoints (docs pulling, vector indexing, system status checking). Directly invokes `src.ingestion` logic. Can handle bulk document ingest and diagnostic searches.

## Conventions

- Always prefix endpoints logically (e.g., `/api/v1/ingest`).
- Use Pydantic models (like `IngestRequest`) to validate required input payloads gracefully.
- Handle exceptions and convert them to `HTTPException`.
