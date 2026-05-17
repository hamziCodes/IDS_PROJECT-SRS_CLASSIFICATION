"""Vercel serverless handler for FastAPI backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import os

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

# Create main app if backend import fails
app = FastAPI(title="Vertex IDS API", version="1.0.0")

# Try to import the backend app
try:
    from app.main import app as backend_app
    app = backend_app
except ImportError as e:
    print(f"Failed to import backend app: {e}")
    print(f"REPO_ROOT: {REPO_ROOT}")
    print(f"backend_path: {backend_path}")
    print(f"backend_path exists: {backend_path.exists()}")
    
    # Create a fallback health endpoint
    @app.get("/health")
    def health():
        return {"status": "error", "message": f"Backend import failed: {str(e)}"}

# Ensure CORS is enabled
if not any(isinstance(m, CORSMiddleware) for m in app.user_middleware):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Export for Vercel
handler = app
