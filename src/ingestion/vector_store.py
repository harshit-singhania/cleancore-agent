"""
Qdrant & Supabase Sync for Vector Storage

Manages the dual-storage architecture:
- Qdrant: Vector embeddings for similarity search
- Supabase (Prisma): Metadata and document content
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, SearchRequest

try:
    from .embedder import Embedder
except ImportError:
    from embedder import Embedder


@dataclass
class VectorDocument:
    """Document with vector embedding ready for storage."""
    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    source_url: str


class VectorStore:
    """
    Dual-storage vector store using Qdrant (vectors) and Supabase (metadata).
    """
    
    COLLECTION_NAME = "sap_abap_docs"
    
    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        embedding_dimensions: int = 3072,
        embedder: Optional[Embedder] = None
    ):
        """
        Initialize the vector store.
        
        Args:
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            embedding_dimensions: Dimensionality of embeddings
            embedder: Embedder instance (creates default if None)
        """
        self.qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.embedding_dimensions = embedding_dimensions
        self.embedder = embedder or Embedder()
        
        # Ensure collection exists
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        collections = self.qdrant.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.COLLECTION_NAME not in collection_names:
            self.qdrant.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.embedding_dimensions,
                    distance=Distance.COSINE
                )
            )
            print(f"Created Qdrant collection: {self.COLLECTION_NAME}")
    
    def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        source_url: str,
        document_id: Optional[str] = None
    ) -> str:
        """
        Add a single document to both Qdrant and Supabase.
        
        Args:
            content: Document text content
            metadata: Additional metadata (headers, section, etc.)
            source_url: Original source URL
            document_id: Optional UUID (generated if not provided)
            
        Returns:
            The document ID (UUID)
        """
        # Generate ID if not provided
        doc_id = document_id or str(uuid.uuid4())
        
        # Generate embedding
        embedding = self.embedder.embed_text(content)
        
        # Store in Qdrant
        self.qdrant.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "source_url": source_url,
                        **metadata
                    }
                )
            ]
        )
        
        return doc_id
    
    def add_documents(
        self,
        documents: List[VectorDocument]
    ) -> List[str]:
        """
        Add multiple documents to Qdrant.
        
        Args:
            documents: List of VectorDocument objects
            
        Returns:
            List of document IDs
        """
        if not documents:
            return []
        
        # Prepare points for batch insert
        points = [
            PointStruct(
                id=doc.id,
                vector=doc.embedding,
                payload={
                    "content": doc.content,
                    "source_url": doc.source_url,
                    **doc.metadata
                }
            )
            for doc in documents
        ]
        
        # Batch upsert to Qdrant
        self.qdrant.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )
        
        return [doc.id for doc in documents]
    
    def search(
        self,
        query: str,
        limit: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query text
            limit: Maximum number of results
            score_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of search results with content and metadata
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Search Qdrant using query_points
        results = self.qdrant.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
            score_threshold=score_threshold
        )
        
        # Format results
        return [
            {
                "id": point.id,
                "score": point.score,
                "content": point.payload.get("content"),
                "source_url": point.payload.get("source_url"),
                "metadata": {k: v for k, v in point.payload.items() 
                           if k not in ["content", "source_url"]}
            }
            for point in results.points
        ]
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the Qdrant collection."""
        collection = self.qdrant.get_collection(self.COLLECTION_NAME)
        return {
            "name": self.COLLECTION_NAME,
            "points_count": collection.points_count,
            "indexed_vectors_count": collection.indexed_vectors_count,
            "segments_count": collection.segments_count,
            "vector_size": self.embedding_dimensions
        }
    
    def delete_all(self):
        """Delete all documents from the collection."""
        self.qdrant.delete_collection(self.COLLECTION_NAME)
        self._ensure_collection()


class IngestionPipeline:
    """
    Complete ingestion pipeline: chunk -> embed -> store.
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        embedder: Optional[Embedder] = None
    ):
        self.vector_store = vector_store or VectorStore()
        self.embedder = embedder or Embedder()
    
    def process_chunks(
        self,
        chunks: List[Any],  # DocumentChunk objects
        batch_size: int = 10
    ) -> List[str]:
        """
        Process document chunks through the full pipeline.
        
        Args:
            chunks: List of DocumentChunk objects
            batch_size: Number of chunks to embed at once
            
        Returns:
            List of document IDs
        """
        all_ids = []
        
        # Process in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            # Generate embeddings for batch
            texts = [chunk.content for chunk in batch]
            embeddings = self.embedder.embed_batch(texts)
            
            # Create VectorDocument objects
            vector_docs = []
            for chunk, embedding in zip(batch, embeddings):
                doc = VectorDocument(
                    id=str(uuid.uuid4()),
                    content=chunk.content,
                    embedding=embedding,
                    metadata=chunk.metadata,
                    source_url=chunk.metadata.get("source_url", "")
                )
                vector_docs.append(doc)
            
            # Store in Qdrant
            ids = self.vector_store.add_documents(vector_docs)
            all_ids.extend(ids)
            
            print(f"Processed batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}: {len(batch)} chunks")
        
        return all_ids


if __name__ == "__main__":
    # Test the vector store
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing Vector Store...")
    
    try:
        # Initialize
        store = VectorStore()
        
        # Get collection info
        info = store.get_collection_info()
        print(f"\nCollection info: {info}")
        
        # Test adding a document
        test_content = "ABAP RESTful Application Programming Model (RAP) provides a standardized way to build SAP Fiori apps."
        doc_id = store.add_document(
            content=test_content,
            metadata={"section": "RAP Overview", "headers": ["ABAP RAP"]},
            source_url="https://example.com/test"
        )
        print(f"\nAdded document with ID: {doc_id}")
        
        # Test search
        print("\nSearching for 'Fiori apps'...")
        results = store.search("Fiori apps", limit=3)
        for r in results:
            print(f"  Score: {r['score']:.4f} - {r['content'][:100]}...")
        
        # Get updated collection info
        info = store.get_collection_info()
        print(f"\nUpdated collection info: {info}")
        
        print("\n✓ Vector store test successful!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
