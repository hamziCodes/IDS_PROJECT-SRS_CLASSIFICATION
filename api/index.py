"""Vercel serverless handler for FastAPI backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add the vertex_app/backend to the path so we can import the app module
backend_path = Path(__file__).parent.parent / "vertex_app" / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

# Import the FastAPI app from the backend
from app.main import app

# Ensure CORS is enabled for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Export the app for Vercel
handler = app
