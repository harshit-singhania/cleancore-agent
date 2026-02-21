# `/src/api` AGENTS.md

## Context

The orchestration layer of the application. It provides the RESTful API endpoints for external clients (the future UI).

## Structure

- `main.py` - FastAPI app initialization, middleware configurations, lifespan definitions (connecting to Prisma/Supabase at startup and disconnecting at shutdown). Start server via `python -m src.api.main`.
- `/routes/` - Dedicated API routers using FastAPI's `APIRouter`.

## Rules

- Keep `main.py` lightweight and focused purely on lifecycle config.
- Business logic is delegated to specific services or modules (like `/ingestion`), whereas routers only format standard JSON payloads and manage HTTP validations.
