"""Stage 4: clean the requirement text and remove duplicates.

Layman: Convert raw requirement sentences into a normalized cleaned column
and remove duplicate or empty items so training data is consistent.
"""

import pandas as pd

from pipeline_common import STAGE2_FILTERED_PATH, STAGE4_CLEANED_PATH, clean_text, ensure_nltk_data


print("[STAGE 4] DATA CLEANING")
print("-" * 100)

# Make sure the tokenizer and lemmatizer resources are available before cleaning text.
ensure_nltk_data()

# Load the filtered dataset so cleaning happens after outlier removal.
combined_df = pd.read_csv(STAGE2_FILTERED_PATH)

# Rebuild the cleaned text column from the raw requirement text for a clean handoff.
combined_df = combined_df.dropna(subset=["RequirementText"])
combined_df["CleanedRequirementText"] = combined_df["RequirementText"].apply(clean_text)

# Remove repeated cleaned rows so the model does not see duplicate examples.
initial_count = len(combined_df)
combined_df.drop_duplicates(subset="CleanedRequirementText", inplace=True)
print(f"  -> Removed duplicate rows: {initial_count - len(combined_df)}")

# Drop empty cleaned texts because they do not add useful signal to the model.
combined_df = combined_df[combined_df["CleanedRequirementText"].str.strip() != ""]
combined_df.reset_index(drop=True, inplace=True)

# Save the cleaned dataset so feature engineering and training use the same text.
STAGE4_CLEANED_PATH.parent.mkdir(parents=True, exist_ok=True)
combined_df.to_csv(STAGE4_CLEANED_PATH, index=False)

# Print a few cleaned samples so we can confirm the transformation is sensible.
print(f"\n✓ Saved cleaned dataset: {STAGE4_CLEANED_PATH}")
print(f"  -> Remaining rows: {len(combined_df)}")
print("\nCleaned text samples:")
for index, (original, cleaned) in enumerate(zip(combined_df["RequirementText"].head(2), combined_df["CleanedRequirementText"].head(2)), start=1):
    print(f"  Sample {index} original: {str(original)[:80]}...")
    print(f"  Sample {index} cleaned : {str(cleaned)[:80]}...")