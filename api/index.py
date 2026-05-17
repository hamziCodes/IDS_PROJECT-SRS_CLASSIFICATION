import sys
from pathlib import Path
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Get the absolute path for the project root
REPO_ROOT = Path(__file__).parent.parent.resolve()

# Add backend and PROJECT to Python path
backend_path = REPO_ROOT / "vertex_app" / "backend"
project_path = REPO_ROOT / "PROJECT"

if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))
if str(project_path) not in sys.path:
    sys.path.insert(0, str(project_path))

# Set environment variable for model paths
os.environ["REPO_ROOT"] = str(REPO_ROOT)

# Create the FastAPI app
app = FastAPI(title="Vertex IDS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import schema classes
try:
    from app.schemas import PredictRequest, PredictResponse, ModelInfoResponse, RequirementItem
    from app.model_loader import get_model_bundle, compute_fr_nfr_metrics
    from app.predictor import run_predictions
    
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

except Exception as e:
    print(f"Error importing backend: {e}")
    @app.get("/health")
    def health() -> dict:
        return {"status": "error", "message": str(e)}
