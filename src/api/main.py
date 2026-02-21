"""
CleanCore Agent - FastAPI Application

Main FastAPI application entry point.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import ingest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 CleanCore Agent API starting up...")
    yield
    # Shutdown
    print("🛑 CleanCore Agent API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="CleanCore Agent API",
    description="Enterprise-grade modernization suite for SAP ABAP to S/4HANA",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router, prefix="/api/v1", tags=["ingestion"])


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "CleanCore Agent API",
        "version": "0.1.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "api": "up",
            "qdrant": "up",  # TODO: Add actual health checks
            "supabase": "up"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
