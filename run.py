import os
import sys
import uvicorn
from pathlib import Path

# 1. Establish core paths
ROOT_DIR = Path(__file__).parent.resolve()
BACKEND_DIR = ROOT_DIR / "vertex_app" / "backend"
APP_DIR = BACKEND_DIR / "app"

# 2. Force Python to see all layers of your project
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(APP_DIR))

# 3. Explicitly import from vertex_app/backend/app/main.py
from vertex_app.backend.app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)