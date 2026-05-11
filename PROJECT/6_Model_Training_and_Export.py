"""Stage 6: train the FR/NFR and NFR-type models and export the artifacts.

Layman: Train a binary model for Functional vs Non-Functional and a
multi-label model for specific NFR categories, then save both models and a
small metadata summary the app can display.
"""

import joblib
import numpy as np
import pandas as pd
import scipy.sparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier

from pipeline_common import (
    MODEL_FR_NFR_PATH,
    MODEL_METADATA_PATH,
    MODEL_NFR_TYPES_PATH,
    NFR_TYPES,
    NFR_TYPES_PATH,
    STAGE4_CLEANED_PATH,
    STAGE5_MATRIX_PATH,
    TRAINED_MODELS_DIR,
)


print("[STAGE 6] MODEL TRAINING AND EXPORT")
print("-" * 100)

# Load the cleaned rows and the saved TF-IDF matrix so the labels match the saved features.
combined_df = pd.read_csv(STAGE4_CLEANED_PATH)
tfidf_matrix = scipy.sparse.load_npz(STAGE5_MATRIX_PATH)

# Pull the FR/NFR label and the NFR subtype labels from the cleaned dataset.
y_fr_nfr = combined_df["IsFunctional"].values if "IsFunctional" in combined_df.columns else np.zeros(len(combined_df))
y_nfr_types = []
for nfr_type in NFR_TYPES:
    if nfr_type in combined_df.columns:
        y_nfr_types.append(combined_df[nfr_type].astype(int).values)
    else:
        y_nfr_types.append(np.zeros(len(combined_df), dtype=int))
y_nfr_types = np.array(y_nfr_types).T

# Split once so both models are trained and evaluated on the same rows.
X_train, X_test, y_train_fr, y_test_fr, y_train_nfr, y_test_nfr = train_test_split(
    tfidf_matrix,
    y_fr_nfr,
    y_nfr_types,
    test_size=0.2,
    random_state=42,
)

# Train the binary FR/NFR classifier with class balancing for the skewed labels.
print("  -> Training FR/NFR classifier...")
model_fr_nfr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
model_fr_nfr.fit(X_train, y_train_fr)
y_pred_fr = model_fr_nfr.predict(X_test)
accuracy_fr = accuracy_score(y_test_fr, y_pred_fr)
print(classification_report(y_test_fr, y_pred_fr, target_names=["Non-Functional", "Functional"]))

# Train the multi-label classifier for NFR subtypes with the same simple model family.
print("  -> Training NFR type classifier...")
model_nfr_types = MultiOutputClassifier(
    LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
)
model_nfr_types.fit(X_train, y_train_nfr)
y_pred_nfr = model_nfr_types.predict(X_test)
accuracy_nfr = accuracy_score(y_test_nfr, y_pred_nfr)
hamming_nfr = hamming_loss(y_test_nfr, y_pred_nfr)
f1_nfr = f1_score(y_test_nfr, y_pred_nfr, average="weighted", zero_division=0)

# Save all artifacts in the same folder the app already expects to use.
TRAINED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model_fr_nfr, MODEL_FR_NFR_PATH)
joblib.dump(model_nfr_types, MODEL_NFR_TYPES_PATH)
np.save(NFR_TYPES_PATH, np.array(NFR_TYPES))

# Save a tiny metadata file so the app can display the training summary later.
metadata = {
    "vocab_size": tfidf_matrix.shape[1],
    "n_samples": len(combined_df),
    "n_train": X_train.shape[0],
    "n_test": X_test.shape[0],
    "accuracy_fr_nfr": accuracy_fr,
    "accuracy_nfr_types": accuracy_nfr,
    "hamming_loss_nfr_types": hamming_nfr,
    "weighted_f1_nfr_types": f1_nfr,
    "nfr_types": NFR_TYPES,
}
joblib.dump(metadata, MODEL_METADATA_PATH)

# Print the final numbers so we know the models trained and exported correctly.
print("\n✓ Model training complete")
print(f"  -> FR/NFR accuracy: {accuracy_fr * 100:.2f}%")
print(f"  -> NFR subset accuracy: {accuracy_nfr * 100:.2f}%")
print(f"  -> NFR Hamming loss: {hamming_nfr:.4f}")
print(f"  -> NFR weighted F1: {f1_nfr:.4f}")
print(f"  -> Saved FR/NFR model: {MODEL_FR_NFR_PATH}")
print(f"  -> Saved NFR type model: {MODEL_NFR_TYPES_PATH}")
print(f"  -> Saved metadata: {MODEL_METADATA_PATH}")