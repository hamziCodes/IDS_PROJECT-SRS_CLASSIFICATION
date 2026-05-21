"""Shared helpers for the split requirement-classification pipeline."""

from pathlib import Path
import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
DATASETS_DIR = ROOT_DIR / "DATASETS"
OUTLIER_MODEL_DIR = ROOT_DIR / "trained_models" / "outlierTrained_model"
TRAINED_MODELS_DIR = ROOT_DIR / "trained_models" / "FR_NFRTrained_models"

ORIGINAL_PROMISE_PATH = DATASETS_DIR / "PROMISE-relabeled-NICE.csv"
PROMISE_CLEANED_PATH = DATASETS_DIR / "PROMISE-relabeled-NICE_cleaned_v1.csv"
SYNTHETIC_PATH = DATASETS_DIR / "synthetic_NFR_augmentation.csv"
SYNTHETIC_CLEANED_PATH = DATASETS_DIR / "synthetic_NFR_augmentation_cleaned_v1.csv"

STAGE1_COMBINED_PATH = DATASETS_DIR / "combined_stage1.csv"
STAGE2_FILTERED_PATH = DATASETS_DIR / "combined_stage2_filtered.csv"
STAGE4_CLEANED_PATH = DATASETS_DIR / "combined_stage4_cleaned.csv"
OUTLIER_REVIEW_BASE_PATH = DATASETS_DIR / "outlier_review.csv"
OUTLIER_REVIEW_PATH = DATASETS_DIR / "outlier_review_from_extra.csv"

STAGE5_MATRIX_PATH = TRAINED_MODELS_DIR / "combined_tfidf_matrix.npz"
STAGE5_VECTORIZER_PATH = TRAINED_MODELS_DIR / "vectorizer_combined.pkl"

OUTLIER_VECTORIZER_PATH = OUTLIER_MODEL_DIR / "outlier_vectorizer.pkl"
OUTLIER_CLASSIFIER_PATH = OUTLIER_MODEL_DIR / "outlier_classifier.pkl"
OUTLIER_METRICS_PATH = OUTLIER_MODEL_DIR / "outlier_metrics.pkl"
OUTLIER_ANOMALY_VECTORIZER_PATH = OUTLIER_MODEL_DIR / "anomaly_vectorizer.pkl"
OUTLIER_ANOMALY_MODEL_PATH = OUTLIER_MODEL_DIR / "anomaly_detector.pkl"

MODEL_FR_NFR_PATH = TRAINED_MODELS_DIR / "model_fr_nfr.pkl"
MODEL_NFR_TYPES_PATH = TRAINED_MODELS_DIR / "model_nfr_types.pkl"
NFR_TYPES_PATH = TRAINED_MODELS_DIR / "nfr_types.npy"
MODEL_METADATA_PATH = TRAINED_MODELS_DIR / "model_metadata.pkl"

NFR_TYPES = [
    "IsQuality",
    "Availability (A)",
    "Fault Tolerance (FT)",
    "Legal (L)",
    "Look & Feel (LF)",
    "Maintainability (MN)",
    "Operability (O)",
    "Performance (PE)",
    "Portability (PO)",
    "Scalability (SC)",
    "Security (SE)",
    "Usability (US)",
    "Other (OT)",
]


def ensure_nltk_data():
    # Download the small NLTK resources the text pipeline needs if they are missing.
    for resource, package in [
        ("tokenizers/punkt", "punkt"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
    ]:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(package, quiet=True)


def load_csv_robust(path):
    # Read CSV files with a strict parser first, then retry with a lenient parser.
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.read_csv(path, engine="python", on_bad_lines="skip", encoding="utf-8")


def clean_text(text):
    # Normalize text with the same simple steps used throughout the original pipeline.
    if pd.isna(text):
        return ""

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    value = str(text).lower()
    value = re.sub(r"[^\w\s]", "", value)
    value = " ".join(word for word in word_tokenize(value) if word not in stop_words)
    value = re.sub(r"\d+", " NUM ", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = " ".join(lemmatizer.lemmatize(word) for word in word_tokenize(value))
    return value


def load_or_create_cleaned_dataset(original_path, cleaned_path, force_recleaning=False):
    # Reuse a fresh cleaned file when possible so the pipeline does not redo work.
    cleaned_path = Path(cleaned_path)
    original_path = Path(original_path)

    if cleaned_path.exists() and not force_recleaning:
        if cleaned_path.stat().st_mtime > original_path.stat().st_mtime:
            return load_csv_robust(cleaned_path)

    # Load the raw CSV and build the cleaned text column from scratch when needed.
    df = load_csv_robust(original_path)
    if "RequirementText" not in df.columns:
        raise ValueError(f"RequirementText column missing in {original_path}")

    # Clean the raw requirement text before saving the versioned file.
    df["CleanedRequirementText"] = df["RequirementText"].apply(clean_text)
    df.drop_duplicates(subset="CleanedRequirementText", inplace=True)
    df = df[df["CleanedRequirementText"].str.strip() != ""]
    df.reset_index(drop=True, inplace=True)

    # Save the cleaned file so later stages can reuse the exact same text version.
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cleaned_path, index=False)
    return df


def basic_outlier_rule(text):
    # Mark obvious greetings, personal intros, and very short text as non-requirements.
    if text is None:
        return True

    value = str(text).strip().lower()
    if value in ["", "nan"]:
        return True
    if len(value.split()) < 3:
        return True

    patterns = [
        r"^my name is\b",
        r"^i am\b",
        r"^hello\b",
        r"^hi\b",
        r"^good morning\b",
        r"^good evening\b",
        r"\bcontact me\b",
    ]
    return any(re.search(pattern, value) for pattern in patterns)


def clean_for_outlier_model(text):
    # Apply the light normalization used by the outlier classifier training script.
    if text is None:
        return ""

    value = str(text).lower().strip()
    if value == "nan":
        return ""

    value = re.sub(r"https?://\S+|www\.\S+", " ", value)
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value