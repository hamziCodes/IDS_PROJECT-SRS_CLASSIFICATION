"""Stage 3: print a simple EDA summary for the filtered dataset.

Layman: Quick checks (shape, missing values, class balance, lengths) so you
can understand the data the model will see.
"""

import pandas as pd

from pipeline_common import STAGE2_FILTERED_PATH


print("[STAGE 3] EXPLORATORY DATA ANALYSIS")
print("-" * 100)

# Load the filtered dataset so the summary reflects the data that will be trained on.
combined_df = pd.read_csv(STAGE2_FILTERED_PATH)

# Print the shape and columns first so we know exactly what the stage received.
print("\nDataset overview:")
print(f"  -> Shape: {combined_df.shape}")
print(f"  -> Columns: {list(combined_df.columns)}")
print(f"  -> Data types:\n{combined_df.dtypes}")

# Check for missing values because the later text pipeline expects complete rows.
missing_data = combined_df.isnull().sum()
if missing_data.sum() > 0:
    print("\nMissing values:")
    print(missing_data[missing_data > 0])
else:
    print("\nNo missing values detected")

# Print the FR/NFR split so we can see whether the classes are balanced.
if "IsFunctional" in combined_df.columns:
    print("\nFunctional requirement distribution:")
    print(combined_df["IsFunctional"].value_counts())
    print(combined_df["IsFunctional"].value_counts(normalize=True))

# Add a quick word-count summary because requirement length is a useful text feature.
combined_df["WordCount"] = combined_df["RequirementText"].apply(lambda value: len(str(value).split()) if pd.notna(value) else 0)
print("\nRequirement text statistics:")
print(f"  -> Average words: {combined_df['WordCount'].mean():.2f}")
print(f"  -> Minimum words: {combined_df['WordCount'].min()}")
print(f"  -> Maximum words: {combined_df['WordCount'].max()}")

# Show a tiny sample so we can verify the rows look like real requirements.
print("\nSample rows:")
print(combined_df[[col for col in ["RequirementText", "IsFunctional"] if col in combined_df.columns]].head(5))