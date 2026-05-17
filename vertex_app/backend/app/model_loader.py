"""Model loading and metrics helpers for the Vertex IDS backend."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support


def _find_repo_root(start_path: Path) -> Path:
    # First check if REPO_ROOT is set in environment (for Vercel)
    if "REPO_ROOT" in os.environ:
        root = Path(os.environ["REPO_ROOT"])
        if (root / "PROJECT").exists() and (root / "trained_models").exists():
            return root
    
    # Fall back to searching parent directories
    for candidate in start_path.parents:
        if (candidate / "PROJECT").exists() and (candidate / "trained_models").exists():
            return candidate
    raise FileNotFoundError("Could not locate the repository root containing PROJECT and trained_models.")


ROOT_DIR = _find_repo_root(Path(__file__).resolve())
PROJECT_DIR = ROOT_DIR / "PROJECT"
if str(PROJECT_DIR) not in sys.path:
    sys.path.append(str(PROJECT_DIR))

from pipeline_common import (  # noqa: E402
    MODEL_FR_NFR_PATH,
    MODEL_METADATA_PATH,
    MODEL_NFR_TYPES_PATH,
    NFR_TYPES_PATH,
    OUTLIER_CLASSIFIER_PATH,
    OUTLIER_VECTORIZER_PATH,
    STAGE4_CLEANED_PATH,
    TRAINED_MODELS_DIR,
    clean_text,
    ensure_nltk_data,
)


@dataclass
class ModelBundle:
    fr_nfr_model: Any
    nfr_type_model: Any
    vectorizer: Any
    nfr_types: List[str]
    metadata: Dict[str, Any]
    outlier_vectorizer: Optional[Any]
    outlier_classifier: Optional[Any]


def _load_or_raise(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing model artifact: {path}")
    return joblib.load(path)


def _load_nfr_types() -> List[str]:
    if NFR_TYPES_PATH.exists():
        return np.load(NFR_TYPES_PATH, allow_pickle=True).tolist()
    if MODEL_NFR_TYPES_PATH.exists():
        metadata = joblib.load(MODEL_METADATA_PATH) if MODEL_METADATA_PATH.exists() else {}
        return metadata.get("nfr_types", [])
    return []


def _load_metadata() -> Dict[str, Any]:
    if MODEL_METADATA_PATH.exists():
        return joblib.load(MODEL_METADATA_PATH)
    return {}


@lru_cache
def get_model_bundle() -> ModelBundle:
    ensure_nltk_data()
    TRAINED_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    fr_nfr_model = _load_or_raise(MODEL_FR_NFR_PATH)
    nfr_type_model = _load_or_raise(MODEL_NFR_TYPES_PATH)
    vectorizer = _load_or_raise(TRAINED_MODELS_DIR / "vectorizer_combined.pkl")
    nfr_types = _load_nfr_types()
    metadata = _load_metadata()

    outlier_vectorizer = None
    outlier_classifier = None
    if OUTLIER_VECTORIZER_PATH.exists() and OUTLIER_CLASSIFIER_PATH.exists():
        outlier_vectorizer = joblib.load(OUTLIER_VECTORIZER_PATH)
        outlier_classifier = joblib.load(OUTLIER_CLASSIFIER_PATH)

    return ModelBundle(
        fr_nfr_model=fr_nfr_model,
        nfr_type_model=nfr_type_model,
        vectorizer=vectorizer,
        nfr_types=nfr_types,
        metadata=metadata,
        outlier_vectorizer=outlier_vectorizer,
        outlier_classifier=outlier_classifier,
    )


def compute_fr_nfr_metrics(bundle: ModelBundle) -> Dict[str, Any]:
    if not STAGE4_CLEANED_PATH.exists():
        return {}

    df = pd.read_csv(STAGE4_CLEANED_PATH)
    if "RequirementText" not in df.columns:
        return {}

    if "CleanedRequirementText" not in df.columns:
        df["CleanedRequirementText"] = df["RequirementText"].apply(clean_text)

    if "IsFunctional" not in df.columns:
        return {}

    texts = df["CleanedRequirementText"].fillna("").astype(str)
    labels = df["IsFunctional"].astype(int).values

    X = bundle.vectorizer.transform(texts)
    preds = bundle.fr_nfr_model.predict(X)

    cm = confusion_matrix(labels, preds, labels=[0, 1])
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary", zero_division=0
    )
    accuracy = accuracy_score(labels, preds)

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "confusion_matrix": cm.tolist(),
        "labels": ["Non-Functional", "Functional"],
        "sample_count": int(len(df)),
        "note": "Metrics computed on full cleaned dataset",
    }
