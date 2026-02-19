"""
CleanCore Agent - FastAPI Backend

AI-powered SAP ABAP modernization tool.
Translates legacy ABAP code into S/4HANA Clean Core compliant code.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

app = FastAPI(
    title="CleanCore Agent API",
    description="API for translating legacy ABAP code to S/4HANA Clean Core compliant code",
    version="1.0.0",
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslateABAPRequest(BaseModel):
    """Request model for ABAP translation."""
    
    code: str = Field(
        ..., 
        description="Legacy ABAP code to be translated",
        min_length=1,
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "REPORT ZTEST.\nDATA: lv_val TYPE string."
            }
        }


class TranslateABAPResponse(BaseModel):
    """Response model for ABAP translation."""
    
    translated_code: str = Field(
        ..., 
        description="Translated S/4HANA Clean Core compliant code"
    )
    status: str = Field(
        default="success",
        description="Translation status"
    )
    message: Optional[str] = Field(
        default=None,
        description="Additional information about the translation"
    )


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    
    error: dict = Field(
        ...,
        description="Error details"
    )


@app.post(
    "/api/v1/translate-abap",
    response_model=TranslateABAPResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid ABAP syntax"},
        500: {"model": ErrorResponse, "description": "Translation service error"},
    },
    summary="Translate legacy ABAP to S/4HANA Clean Core",
    description="Accepts legacy ABAP code and returns S/4HANA Clean Core compliant code using AI translation.",
)
async def translate_abap(request: TranslateABAPRequest) -> TranslateABAPResponse:
    """
    Translate legacy ABAP code to S/4HANA Clean Core compliant code.
    
    This endpoint:
    - Accepts raw ABAP code as input
    - Processes it using Gemini 1.5 Flash (future implementation)
    - Returns RAP-compliant ABAP code
    
    **Note:** Currently returns dummy translated code for scaffolding purposes.
    """
    # TODO: Implement actual Gemini 1.5 Flash translation logic
    # For now, return dummy translated code
    
    dummy_translated = f"""* CleanCore Agent - Translated Output (DEMO)
* Original code processed: {len(request.code)} characters
* Status: This is a placeholder response

CLASS zcl_demo_clean_core DEFINITION PUBLIC.
  PUBLIC SECTION.
    METHODS process_data
      IMPORTING iv_input TYPE string
      RETURNING VALUE(rv_output) TYPE string
      RAISING cx_static_check.
ENDCLASS.

CLASS zcl_demo_clean_core IMPLEMENTATION.
  METHOD process_data.
    " TODO: Implement RAP-compliant logic here
    rv_output = |Processed: {{ iv_input }}|.
  ENDMETHOD.
ENDCLASS."""

    return TranslateABAPResponse(
        translated_code=dummy_translated,
        status="success",
        message="Translation completed (dummy response for scaffolding)",
    )


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "service": "CleanCore Agent API",
        "version": "1.0.0",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
