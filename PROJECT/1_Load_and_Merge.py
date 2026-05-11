"""Stage 1: load the source datasets and merge them into one file.

Layman: Read cleaned PROMISE and synthetic files, concatenate them into
one combined CSV that later stages will use.
"""

import pandas as pd

from pipeline_common import (
    ORIGINAL_PROMISE_PATH,
    PROMISE_CLEANED_PATH,
    STAGE1_COMBINED_PATH,
    SYNTHETIC_CLEANED_PATH,
    SYNTHETIC_PATH,
    ensure_nltk_data,
    load_or_create_cleaned_dataset,
)


print("[STAGE 1] LOAD AND MERGE DATASETS")
print("-" * 100)

# Make sure the text tools exist before we touch any requirement text (download NLTK data if missing).
ensure_nltk_data()

# Load or create the cleaned PROMISE dataset so every later stage sees the same text.
print("  -> Loading PROMISE dataset...")
promise_df = load_or_create_cleaned_dataset(ORIGINAL_PROMISE_PATH, PROMISE_CLEANED_PATH)
print(f"  -> PROMISE ready: {promise_df.shape[0]} rows, {promise_df.shape[1]} columns")

# Load or create the cleaned synthetic dataset so the merged training set stays consistent.
print("  -> Loading synthetic NFR dataset...")
synthetic_df = load_or_create_cleaned_dataset(SYNTHETIC_PATH, SYNTHETIC_CLEANED_PATH)
print(f"  -> Synthetic NFR ready: {synthetic_df.shape[0]} rows, {synthetic_df.shape[1]} columns")

# Merge the two datasets into one combined file for the rest of the pipeline.
combined_df = pd.concat([promise_df, synthetic_df], ignore_index=True)
STAGE1_COMBINED_PATH.parent.mkdir(parents=True, exist_ok=True)
combined_df.to_csv(STAGE1_COMBINED_PATH, index=False)

# Print the final shape so we can confirm the merge worked before moving on.
print(f"\n✓ Saved combined dataset: {STAGE1_COMBINED_PATH}")
print(f"  -> Combined shape: {combined_df.shape}")