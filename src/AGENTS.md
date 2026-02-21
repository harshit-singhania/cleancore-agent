# `/src` AGENTS.md

## Context

This directory contains the Python logic driving CleanCore Agent.

## Directory Structure

- `/api/` - The FastAPI application framework and routes.
- `/ingestion/` - The Knowledge Ingestion and RAG capabilities.

## Code Conventions

- Strongly-typed Python 3.11+ using explicit return types and Pydantic schemas where applicable.
- The entry point runs using `uvicorn` (currently exposed in `api.main`).
- Database logic binds directly with Prisma's Python client.

See subdirectories for specific context.
