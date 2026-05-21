# Vertex IDS Backend

FastAPI service that loads the trained IDS NLP models and exposes prediction and model-info endpoints.

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

- `GET /health`
- `POST /predict`
- `GET /model-info`

### Example request

```json
{
  "text": "The system shall encrypt all user data at rest.\nThe system shall allow users to reset passwords.",
  "force_classify": false
}
```
