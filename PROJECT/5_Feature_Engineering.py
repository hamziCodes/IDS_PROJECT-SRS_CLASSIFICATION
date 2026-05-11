"""Stage 5: turn cleaned text into TF-IDF features and save the vectorizer.

Layman: Convert cleaned requirement text into numeric TF-IDF features the
models can understand, then save the vectorizer and sparse matrix.
"""

import joblib
import pandas as pd
import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer

from pipeline_common import STAGE4_CLEANED_PATH, STAGE5_MATRIX_PATH, STAGE5_VECTORIZER_PATH, TRAINED_MODELS_DIR


print("[STAGE 5] FEATURE ENGINEERING")
print("-" * 100)

# Load the cleaned dataset so the feature matrix matches the final cleaned text.
combined_df = pd.read_csv(STAGE4_CLEANED_PATH)

# Build a simple TF-IDF vectorizer with the same settings used in the original script.
print("  -> Initializing TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2, max_df=0.95)

# Fit the vectorizer and convert the text into a sparse numeric matrix.
print("  -> Fitting and transforming cleaned text...")
tfidf_matrix = vectorizer.fit_transform(combined_df["CleanedRequirementText"])

# Save the vectorizer and matrix so training can reuse the exact same features later.
TRAINED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(vectorizer, STAGE5_VECTORIZER_PATH)
scipy.sparse.save_npz(STAGE5_MATRIX_PATH, tfidf_matrix)

# Print a short summary so we can verify the feature space size and sparsity.
print(f"\n✓ Saved vectorizer: {STAGE5_VECTORIZER_PATH}")
print(f"✓ Saved TF-IDF matrix: {STAGE5_MATRIX_PATH}")
print(f"  -> Matrix shape: {tfidf_matrix.shape}")
print(f"  -> Sparsity: {(1 - tfidf_matrix.nnz / (tfidf_matrix.shape[0] * tfidf_matrix.shape[1])) * 100:.2f}%")
print(f"  -> Vocabulary size: {tfidf_matrix.shape[1]}")