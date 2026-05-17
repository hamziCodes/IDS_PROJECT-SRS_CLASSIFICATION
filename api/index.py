from __future__ import annotations

import sys
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend path is importable when running on Vercel
REPO_ROOT = Path(__file__).parent.parent.resolve()
backend_path = REPO_ROOT / "vertex_app" / "backend"

# Only insert the backend API path to prevent Streamlit collisions
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

os.environ.setdefault("REPO_ROOT", str(REPO_ROOT))

app = FastAPI(title="Vertex IDS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(payload: dict):
    """Lazy-loads models and runs prediction. Returns 503 if models are not available."""
    try:
        from app.model_loader import get_model_bundle
        from app.predictor import run_predictions
        # RequirementItem is only used to format results if available
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model backend not available: {e}")

    text = payload.get("text") if isinstance(payload, dict) else None
    force = payload.get("force_classify", False) if isinstance(payload, dict) else False
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' in request body")

    try:
        bundle = get_model_bundle()
        result = run_predictions(bundle, text, force)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}") from e

    def to_dict(items):
        return [getattr(item, "__dict__", item) for item in items]

    return {
        "functional_requirements": to_dict(result.get("functional_requirements", [])),
        "non_functional_requirements": to_dict(result.get("non_functional_requirements", [])),
        "neither": to_dict(result.get("neither", [])),
        "items": to_dict(result.get("items", [])),
        "counts": result.get("counts", {}),
    }


@app.get("/model-info")
def model_info():
    try:
        from app.model_loader import get_model_bundle, compute_fr_nfr_metrics
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model backend not available: {e}")

    try:
        bundle = get_model_bundle()
        metrics = compute_fr_nfr_metrics(bundle)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model info: {e}") from e

    return {
        "model_name": "Vertex Requirement Classifier",
        "version": "1.0.0",
        "metrics": metrics,
        "nfr_types": getattr(bundle, "nfr_types", []),
        "metadata": getattr(bundle, "metadata", {}),
    }