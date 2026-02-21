# CleanCore AGENTS.md

This document serves as the top-level architectural map for AI agents (and human developers) navigating the `cleancore-agent` repository.

## Directory Map

| Path | Purpose | Key Technologies |
|------|---------|------------------|
| `/` | Root project and services orchestrator | Node/npm for Prisma, `dev.sh`, `.env.local` |
| `/prisma` | Database schema and migrations | Prisma interact with Supabase |
| `/src` | Main Application Source Code | Python 3.11+, FastAPI |
| `/src/api` | Fast API orchestration and lifecycle | FastAPI, Pydantic |
| `/src/api/routes` | Defined API endpoints | FastAPI Routers |
| `/src/ingestion` | RAG ingestion pipeline | Gemini Embeddings, Qdrant, Markdown Chunker |
| `/tests` | Automated testing | pytest |
| `/.gsd` | (GitIgnored) GSD agent state and tasks | Markdown |

## Architectural Overview

CleanCore Agent 2.0 acts as a high-speed copilot for ABAP architects to modernize legacy code to ABAP Cloud/RAP.

1. **Phase 1: Foundation (Data Layer)**
   - **Supabase (Prisma):** Handles all relational metadata (Users, Projects, Translation Results, Documents).
   - **Qdrant:** Handles 768-dimensional vector matching for ABAP documentation. Runs locally via Colima.

2. **Phase 2: Knowledge Ingestion**
   - **Data Sourcing:** SAP's public GitHub cheat sheets.
   - **Chunking:** Semantic Markdown structure (preserves headers).
   - **Embeddings:** `text-embedding-004` (Google GenAI).

## Commands

- `colima start` / `colima stop` — Start Qdrant environment
- `docker-compose up -d qdrant` — Start vector DB
- `./dev.sh start` — Run FastAPI backend (localhost:8080)
- `npm run dev` (If frontend exists)

Explore the `AGENTS.md` files in each subdirectory for detailed agentic contexts.
