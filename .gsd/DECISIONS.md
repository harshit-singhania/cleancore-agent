# Architectural Decisions

## Phase 1: Foundation (Setup & Data Layer)

*Date: 2026-02-21*

### 1. Data Schema & Multi-Tenancy

* **Decision:** Implement multi-tenant isolation right away (User/Org relations) rather than tracking projects globally.
* **Rationale:** Ensures data security and scalability from the beginning, matching enterprise requirements.

### 2. Metadata Tracking (MVP)

* **Decision:** The MVP will track specific metadata fields for `CodeObject` and `TranslationResult`: ABAP object type, legacy LOC, token count, and processing type.
* **Rationale:** Provides necessary analytics and tracking for the translation pipeline without over-engineering the initial schema.

### 3. Vector Database Deployment

* **Decision:** Use a local Docker cluster for Qdrant during development.
* **Rationale:** Saves costs and simplifies the local developer experience.

### 4. Document Embedding Strategy

* **Decision:** Prepare the Prisma schema to support vector embeddings for documentation, aligning with the planned Qdrant integration.
* **Rationale:** Ensures the foundation is ready for Phase 2 (Knowledge Ingestion) without needing structural database changes later.
