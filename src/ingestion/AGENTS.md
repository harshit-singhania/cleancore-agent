# `/src/ingestion` AGENTS.md

## Context

Holds the RAG augmentation engines and document ingestion workers utilized during Phase 2.

## Modules

- `markdown_chunker.py` - Downloads raw SAP `.md` reference files from their official sources (like `SAP-samples/abap-cheat-sheets`), parses them structure-wise using `langchain_text_splitters` `MarkdownHeaderTextSplitter`, and groups headers and contextual code securely together.
- `embedder.py` - Interacts with Google's newer Generative AI client using `text-embedding-004` (768 dimensions).
- `vector_store.py` - Syncs data between local Qdrant collection (`sap_abap_docs`) and Supabase via Postgres/Prisma. Ensures `qdrantId` pairs consistently across both architectures.

## Execution

This domain is currently orchestrated synchronously by the `/api` routes (as per the MVP), but built modularly enough to handle async / queue-based ingestions if required natively in the future.
