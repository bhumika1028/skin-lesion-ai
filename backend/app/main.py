import sys
import os
from pathlib import Path

# Add project root directory to sys.path so modules resolve correctly
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router as api_router

app = FastAPI(
    title="AI-Based Skin Lesion Uncertainty-Aware Risk Triage API",
    description="Multimodal Swin Transformer + Clinical Metadata + Dirichlet Evidential Deep Learning (EDL) Triage Backend.",
    version="1.0.0"
)

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the AI-Based Skin Lesion Uncertainty-Aware Risk Triage API",
        "documentation": "/docs",
        "health_check": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
