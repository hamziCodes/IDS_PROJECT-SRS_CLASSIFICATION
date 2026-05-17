"""FastAPI entrypoint for the Vertex IDS backend."""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .model_loader import compute_fr_nfr_metrics, get_model_bundle
from .predictor import run_predictions
from .schemas import ModelInfoResponse, PredictRequest, PredictResponse, RequirementItem


app = FastAPI(title="Vertex IDS API", version="1.0.0")
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {
        "status": "ok",
        "message": "Vertex IDS API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "model-info": "/model-info"
        }
    }


@app.on_event("startup")
def warm_models() -> None:
    get_model_bundle()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    try:
        bundle = get_model_bundle()
        result = run_predictions(bundle, request.text, request.force_classify)
    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed") from error

    def to_schema(items):
        return [RequirementItem(**item.__dict__) for item in items]

    return PredictResponse(
        functional_requirements=to_schema(result["functional_requirements"]),
        non_functional_requirements=to_schema(result["non_functional_requirements"]),
        neither=to_schema(result["neither"]),
        items=to_schema(result["items"]),
        counts=result["counts"],
    )


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    bundle = get_model_bundle()
    metrics = compute_fr_nfr_metrics(bundle)

    return ModelInfoResponse(
        model_name="Vertex Requirement Classifier",
        version="1.0.0",
        metrics=metrics,
        nfr_types=bundle.nfr_types,
        metadata=bundle.metadata,
    )
