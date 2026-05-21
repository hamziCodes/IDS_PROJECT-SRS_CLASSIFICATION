"""Prediction utilities for the Vertex IDS backend."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import re
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = ROOT_DIR / "PROJECT"
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pipeline_common import basic_outlier_rule, clean_for_outlier_model, clean_text


@dataclass
class PredictionItem:
    text: str
    label: str
    confidence: Optional[float]
    nfr_types: List[str]
    outlier_probability: Optional[float]
    is_outlier: bool


def split_requirements(text: str) -> List[str]:
    if not text:
        return []

    raw = text.strip()
    # Split on newlines first, then on bullet-like markers.
    lines = re.split(r"[\r\n]+", raw)
    chunks: List[str] = []
    for line in lines:
        line = re.sub(r"^\s*[-*]+\s*", "", line)
        line = re.sub(r"^\s*\d+\.|^\s*\d+\)\s*", "", line)
        if line.strip():
            chunks.append(line.strip())

    if len(chunks) == 1:
        # If a single long paragraph, fall back to sentence-ish splitting.
        if len(chunks[0].split()) > 20:
            parts = re.split(r"(?<=[.!?;])\s+", chunks[0])
            parts = [p.strip() for p in parts if p.strip()]
            return parts if parts else chunks
    return chunks


def _predict_single(bundle: Any, text: str, force_classify: bool) -> PredictionItem:
    outlier_probability = None
    is_rule_outlier = basic_outlier_rule(text)
    is_model_outlier = False

    if bundle.outlier_vectorizer is not None and bundle.outlier_classifier is not None:
        try:
            outlier_matrix = bundle.outlier_vectorizer.transform([clean_for_outlier_model(text)])
            outlier_probability = float(bundle.outlier_classifier.predict_proba(outlier_matrix)[0][1])
            is_model_outlier = outlier_probability >= 0.4
        except Exception:
            outlier_probability = None
            is_model_outlier = False

    is_outlier = is_rule_outlier or is_model_outlier

    if is_outlier and not force_classify:
        return PredictionItem(
            text=text,
            label="neither",
            confidence=None,
            nfr_types=[],
            outlier_probability=outlier_probability,
            is_outlier=True,
        )

    cleaned_text = clean_text(text)
    vector = bundle.vectorizer.transform([cleaned_text])
    fr_nfr_pred = int(bundle.fr_nfr_model.predict(vector)[0])
    fr_nfr_proba = bundle.fr_nfr_model.predict_proba(vector)[0]

    if fr_nfr_pred == 1:
        label = "functional"
        confidence = float(fr_nfr_proba[1])
        nfr_types: List[str] = []
    else:
        label = "non_functional"
        confidence = float(fr_nfr_proba[0])
        nfr_pred = bundle.nfr_type_model.predict(vector)[0]
        nfr_types = [name for name, flag in zip(bundle.nfr_types, nfr_pred) if int(flag) == 1]

    return PredictionItem(
        text=text,
        label=label,
        confidence=confidence,
        nfr_types=nfr_types,
        outlier_probability=outlier_probability,
        is_outlier=is_outlier,
    )


def run_predictions(bundle: Any, text: str, force_classify: bool = False) -> Dict[str, Any]:
    items: List[PredictionItem] = []
    for chunk in split_requirements(text):
        items.append(_predict_single(bundle, chunk, force_classify))

    functional = [item for item in items if item.label == "functional"]
    non_functional = [item for item in items if item.label == "non_functional"]
    neither = [item for item in items if item.label == "neither"]

    return {
        "items": items,
        "functional_requirements": functional,
        "non_functional_requirements": non_functional,
        "neither": neither,
        "counts": {
            "functional": len(functional),
            "non_functional": len(non_functional),
            "neither": len(neither),
            "total": len(items),
        },
    }
