import os
import sys
import uvicorn
from pathlib import Path

# 1. Get the exact paths to your folders
ROOT_DIR = Path(__file__).parent.resolve()
BACKEND_DIR = ROOT_DIR / "vertex_app" / "backend"

# 2. Force Python to see both the root (for pipeline_common) and the backend (for app.model_loader)
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(BACKEND_DIR))

# 3. Now that Python can see everything, import the FastAPI app safely
from index import app

if __name__ == "__main__":
    # Render assigns a dynamic port via environment variables
    port = int(os.environ.get("PORT", 10000))
    
    # 4. Boot the server directly from Python
    uvicorn.run(app, host="0.0.0.0", port=port)