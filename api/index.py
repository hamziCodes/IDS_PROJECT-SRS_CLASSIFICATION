import sys
from pathlib import Path

# Tell Vercel where the root of your repository is (one level up from /api)
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import your actual FastAPI app from your clean folder structure
from vertex_app.backend.index import app