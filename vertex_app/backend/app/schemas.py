"""API schemas for the Vertex IDS backend."""

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Requirement text to classify")
    force_classify: bool = Field(False, description="Override outlier gate")


class RequirementItem(BaseModel):
    text: str
    label: str
    confidence: Optional[float] = None
    nfr_types: List[str] = Field(default_factory=list)
    outlier_probability: Optional[float] = None
    is_outlier: bool = False


class PredictResponse(BaseModel):
    functional_requirements: List[RequirementItem]
    non_functional_requirements: List[RequirementItem]
    neither: List[RequirementItem]
    items: List[RequirementItem]
    counts: Dict[str, int]


class ModelInfoResponse(BaseModel):
    model_name: str
    version: str
    metrics: Dict[str, object]
    nfr_types: List[str]
    metadata: Dict[str, object]
