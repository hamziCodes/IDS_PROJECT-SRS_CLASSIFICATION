# Vertex App

Flutter client for the Vertex IDS classifier.

## Run the backend first

The app calls the FastAPI service in [backend/app/main.py](backend/app/main.py).

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Run the Flutter app

For Chrome/web, the app now uses `http://localhost:8000` by default.

For an Android emulator, it uses `http://10.0.2.2:8000` by default.

You can override the API host explicitly:

```bash
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```

## Notes

- The trained model artifacts live in [../trained_models/FR_NFRTrained_models](../trained_models/FR_NFRTrained_models) and [../trained_models/outlierTrained_model](../trained_models/outlierTrained_model).
- The backend applies the same outlier gate and FR/NFR logic used by the training pipeline.
