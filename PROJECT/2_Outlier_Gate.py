"""Stage 2: filter obvious outliers before FR/NFR training.

Layman: Use a few cheap rules plus the trained outlier model (if available)
to mark and remove texts that are not real software requirements.
"""

from pathlib import Path

import joblib
import pandas as pd

from pipeline_common import (
    OUTLIER_MODEL_DIR,
    OUTLIER_REVIEW_PATH,
    STAGE1_COMBINED_PATH,
    STAGE2_FILTERED_PATH,
    basic_outlier_rule,
    clean_for_outlier_model,
)


print("[STAGE 2] OUTLIER GATE")
print("-" * 100)

# Read the merged dataset from stage 1 so outlier filtering works on the shared input.
combined_df = pd.read_csv(STAGE1_COMBINED_PATH)

# Add a cheap rule-based signal that catches obvious non-requirements.
combined_df["IsOutlierRule"] = combined_df["RequirementText"].apply(basic_outlier_rule).astype(int)
combined_df["OutlierProbability"] = 0.0
combined_df["IsOutlierModel"] = 0

# Load the trained outlier model only when the Stage 0 artifacts are available.
# If present, use it to score each text; otherwise fall back to rule-based checks.
vectorizer_path = Path(OUTLIER_MODEL_DIR) / "outlier_vectorizer.pkl"
classifier_path = Path(OUTLIER_MODEL_DIR) / "outlier_classifier.pkl"

if vectorizer_path.exists() and classifier_path.exists():
    print("  -> Loading trained outlier model artifacts...")
    outlier_vectorizer = joblib.load(vectorizer_path)
    outlier_classifier = joblib.load(classifier_path)

    # Score each text with the same normalization used by the outlier training script.
    normalized_text = combined_df["RequirementText"].apply(clean_for_outlier_model)
    outlier_matrix = outlier_vectorizer.transform(normalized_text)
    combined_df["OutlierProbability"] = outlier_classifier.predict_proba(outlier_matrix)[:, 1]
    combined_df["IsOutlierModel"] = (combined_df["OutlierProbability"] >= 0.40).astype(int)
    print("  -> Outlier model scoring complete")
else:
    print("  -> Outlier model files not found, so rule-based filtering only will be used")

# Combine both signals so one strong warning is enough to filter a row out.
combined_df["IsOutlierFinal"] = ((combined_df["IsOutlierRule"] == 1) | (combined_df["IsOutlierModel"] == 1)).astype(int)

# Save the review file so we can inspect what was removed and why.
OUTLIER_REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
combined_df[["RequirementText", "IsOutlierRule", "OutlierProbability", "IsOutlierModel", "IsOutlierFinal"]].to_csv(
    OUTLIER_REVIEW_PATH,
    index=False,
)
print(f"  -> Saved outlier review file: {OUTLIER_REVIEW_PATH}")

# Keep only rows that are safe to train on and save them for the next stage.
filtered_df = combined_df[combined_df["IsOutlierFinal"] == 0].copy()
filtered_df.reset_index(drop=True, inplace=True)
filtered_df.to_csv(STAGE2_FILTERED_PATH, index=False)

# Print the kept row count so we can confirm the filter behaved as expected.
print(f"  -> Outliers flagged: {int(combined_df['IsOutlierFinal'].sum())}")
print(f"  -> Rows kept: {len(filtered_df)}")
print(f"\n✓ Saved filtered dataset: {STAGE2_FILTERED_PATH}")