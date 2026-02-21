"""
Ingestion API Routes

Endpoints for ingesting SAP documentation into the vector store.
"""

import sys
import os
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from ingestion.markdown_chunker import MarkdownChunker, SAP_CHEAT_SHEET_URLS
    from ingestion.vector_store import IngestionPipeline, VectorStore
    from ingestion.embedder import Embedder
except ImportError:
    # Fallback for direct execution
    from src.ingestion.markdown_chunker import MarkdownChunker, SAP_CHEAT_SHEET_URLS
    from src.ingestion.vector_store import IngestionPipeline, VectorStore
    from src.ingestion.embedder import Embedder


router = APIRouter()


class IngestRequest(BaseModel):
    """Request body for ingestion endpoint."""
    urls: Optional[List[str]] = None
    batch_size: int = 10


class IngestResponse(BaseModel):
    """Response from ingestion endpoint."""
    success: bool
    message: str
    documents_processed: int
    chunks_created: int
    collection_info: Optional[dict] = None


@router.post("/ingest/docs", response_model=IngestResponse)
async def ingest_documents(
    request: IngestRequest
):
    """
    Ingest SAP ABAP documentation into the vector store.
    
    Downloads markdown from specified URLs (or defaults to SAP cheat sheets),
    chunks them semantically, generates embeddings, and stores in Qdrant.
    
    Args:
        request: Ingestion configuration including URLs and batch size
        
    Returns:
        Ingestion statistics and collection info
    """
    try:
        # Use default URLs if none provided
        urls = request.urls or SAP_CHEAT_SHEET_URLS
        
        # Initialize components
        chunker = MarkdownChunker()
        vector_store = VectorStore()
        pipeline = IngestionPipeline(vector_store=vector_store)
        
        # Track statistics
        total_chunks = 0
        documents_processed = 0
        
        # Process each URL
        for url in urls:
            try:
                # Download and chunk
                chunks = chunker.process_url(url)
                documents_processed += 1
                
                if not chunks:
                    continue
                
                # Process chunks through pipeline
                doc_ids = pipeline.process_chunks(chunks, batch_size=request.batch_size)
                total_chunks += len(doc_ids)
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        # Get collection info
        collection_info = vector_store.get_collection_info()
        
        return IngestResponse(
            success=True,
            message=f"Successfully ingested {total_chunks} chunks from {documents_processed} documents",
            documents_processed=documents_processed,
            chunks_created=total_chunks,
            collection_info=collection_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )


@router.get("/ingest/status")
async def get_ingestion_status():
    """
    Get current ingestion status and collection statistics.
    
    Returns:
        Collection information and document counts
    """
    try:
        vector_store = VectorStore()
        collection_info = vector_store.get_collection_info()
        
        return {
            "status": "ready",
            "collection": collection_info
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get status: {str(e)}"
        )


@router.post("/ingest/search")
async def search_documents(query: str, limit: int = 5):
    """
    Search for documents in the vector store.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        
    Returns:
        List of matching documents with similarity scores
    """
    try:
        vector_store = VectorStore()
        results = vector_store.search(query, limit=limit)
        
        return {
            "query": query,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
