"""
Gemini Embedding Client for Vector Generation

Generates vector embeddings using Google's text-embedding-004 model.
"""

import os
from typing import List, Union
from google import genai
from google.genai import types

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


class Embedder:
    """
    Client for generating text embeddings using Google's Gemini API.
    
    Uses the text-embedding-004 model which outputs 768-dimensional vectors.
    """
    
    MODEL_NAME = "models/gemini-embedding-001"
    EMBEDDING_DIMENSIONS = 3072
    
    def __init__(self, api_key: str = None):
        """
        Initialize the embedder with API key.
        
        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key required. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = genai.Client(api_key=self.api_key)
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of 768 float values representing the embedding vector
        """
        result = self.client.models.embed_content(
            model=self.MODEL_NAME,
            contents=text,
        )
        return result.embeddings[0].values
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process per API call
            
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            result = self.client.models.embed_content(
                model=self.MODEL_NAME,
                contents=batch,
            )
            
            batch_embeddings = [emb.values for emb in result.embeddings]
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
    
    def get_dimensions(self) -> int:
        """Return the embedding dimensions for this model."""
        return self.EMBEDDING_DIMENSIONS


if __name__ == "__main__":
    # Test the embedder
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing Gemini Embedder...")
    print(f"Model: {Embedder.MODEL_NAME}")
    print(f"Dimensions: {Embedder.EMBEDDING_DIMENSIONS}")
    
    try:
        embedder = Embedder()
        
        # Test single embedding
        test_text = "ABAP RESTful Application Programming Model (RAP)"
        print(f"\nEmbedding text: '{test_text}'")
        
        embedding = embedder.embed_text(test_text)
        print(f"Embedding dimensions: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
        
        # Test batch embedding
        test_texts = [
            "ABAP SQL syntax",
            "Core Data Services (CDS)",
            "RAP business objects"
        ]
        print(f"\nBatch embedding {len(test_texts)} texts...")
        
        batch_embeddings = embedder.embed_batch(test_texts)
        print(f"Generated {len(batch_embeddings)} embeddings")
        print(f"Each embedding has {len(batch_embeddings[0])} dimensions")
        
        print("\n✓ Embedder test successful!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
