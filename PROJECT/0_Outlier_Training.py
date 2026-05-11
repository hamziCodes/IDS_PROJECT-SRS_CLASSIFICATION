"""Stage 0: train the outlier detector before the main requirement pipeline."""

import argparse
import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

from pipeline_common import (
    DATASETS_DIR,
    OUTLIER_ANOMALY_MODEL_PATH,
    OUTLIER_ANOMALY_VECTORIZER_PATH,
    OUTLIER_CLASSIFIER_PATH,
    OUTLIER_METRICS_PATH,
    OUTLIER_MODEL_DIR,
    OUTLIER_REVIEW_BASE_PATH,
    OUTLIER_VECTORIZER_PATH,
    clean_text,
    ensure_nltk_data,
)


warnings.filterwarnings("ignore")

LOCAL_REQUIREMENT_FILES = [
    "PROMISE-relabeled-NICE.csv",
    "PROMISE-relabeled-NICE_cleaned_v1.csv",
    "synthetic_NFR_augmentation.csv",
    "synthetic_NFR_augmentation_cleaned_v1.csv",
]


def guess_text_column(df):
    # Choose the most likely column that contains textual content (simple heuristic).
    # This helps the stage work with different CSV schemas by guessing the text field.
    preferred = ["text", "sentence", "utterance", "content", "query", "prompt", "requirementtext", "response"]
    lower_map = {column.lower(): column for column in df.columns}
    for name in preferred:
        if name in lower_map:
            return lower_map[name]
    for column in df.columns:
        if df[column].dtype == object:
            return column
    return df.columns[0] if len(df.columns) > 0 else None


def load_local_requirements():
    # Load local CSVs and mark them as "real requirements" (inlier examples).
    # Returns a DataFrame with columns: text, source, label(0=inlier).
    parts = []
    for file_name in LOCAL_REQUIREMENT_FILES:
        file_path = DATASETS_DIR / file_name
        if not file_path.exists():
            continue

        try:
            df = pd.read_csv(file_path, engine="python", on_bad_lines="skip", encoding="utf-8")
        except Exception:
            continue

        text_col = guess_text_column(df)
        if text_col is None:
            continue

        parts.append(
            pd.DataFrame(
                {
                    "text": df[text_col].astype(str),
                    "source": file_name.replace(".csv", ""),
                    "label": 0,
                }
            )
        )

    if not parts:
        return pd.DataFrame(columns=["text", "source", "label"])
    return pd.concat(parts, ignore_index=True)


def load_hf_outliers(max_rows_per_split=5000):
    # Pull public text corpora from Hugging Face to act as obvious non-requirement examples.
    # These are labeled as outliers so the classifier learns a clear separation.
    from datasets import load_dataset

    specs = [
        {"dataset": "Salesforce/wikitext", "config": "wikitext-103-raw-v1", "splits": ["train"], "name": "wikitext"},
        {
            "dataset": "AlekseyKorshuk/persona-chat",
            "config": None,
            "splits": ["train", "validation", "test"],
            "name": "persona_chat",
        },
        {
            "dataset": "DeepPavlov/clinc150",
            "config": "default",
            "splits": ["train", "validation", "test"],
            "name": "clinc150_oos",
        },
    ]

    parts = []
    for spec in specs:
        print(f"Loading {spec['dataset']}...")
        try:
            ds = load_dataset(spec["dataset"], spec["config"]) if spec["config"] else load_dataset(spec["dataset"])
        except Exception as error:
            print(f"  skip dataset because: {error}")
            continue

        for split in spec["splits"]:
            if split not in ds:
                continue

            try:
                one_split = ds[split]
                if max_rows_per_split and len(one_split) > max_rows_per_split:
                    one_split = one_split.select(range(max_rows_per_split))
                df = one_split.to_pandas()
                text_col = guess_text_column(df)
                if text_col is None:
                    continue

                parts.append(
                    pd.DataFrame(
                        {
                            "text": df[text_col].astype(str),
                            "source": f"{spec['name']}_{split}",
                            "label": 1,
                        }
                    )
                )
            except Exception as error:
                print(f"  skip split {split} because: {error}")

    if not parts:
        return pd.DataFrame(columns=["text", "source", "label"])
    return pd.concat(parts, ignore_index=True)


def main():
    # Train a simple binary classifier that separates real requirements (inliers)
    # from general text (outliers). The unsupervised anomaly detector is optional.
    parser = argparse.ArgumentParser(description="Train the outlier classifier used before the main pipeline")
    parser.add_argument("--no-anomaly-detector", action="store_true", help="skip IsolationForest")
    parser.add_argument("--max-rows-per-split", type=int, default=5000, help="rows to pull from each HF split")
    args = parser.parse_args()

    # Make sure the NLTK resources used by the shared cleanup function are present.
    ensure_nltk_data()

    # Load your project requirement text as the inlier class.
    print("Loading local requirement texts...")
    req_df = load_local_requirements()

    # Load external text data as the outlier class.
    print("Loading Hugging Face outlier texts...")
    out_df = load_hf_outliers(max_rows_per_split=args.max_rows_per_split)

    # Combine both classes so the model can learn the boundary between them.
    corpus = pd.concat([req_df, out_df], ignore_index=True)
    if corpus.empty:
        raise RuntimeError("No data loaded. Check DATASETS files and HF access.")

    # Apply the same light cleanup used by the rest of the project.
    corpus["text"] = corpus["text"].map(clean_text)
    corpus = corpus[corpus["text"].str.strip() != ""].copy()
    corpus = corpus.drop_duplicates(subset=["text", "label"]).reset_index(drop=True)

    print("\nCorpus summary:")
    print(corpus.groupby(["label", "source"]).size().reset_index(name="count"))

    # Train the binary outlier classifier.
    print("\nTraining binary classifier (0=requirement, 1=outlier)...")
    X_train, X_test, y_train, y_test = train_test_split(
        corpus["text"],
        corpus["label"].astype(int),
        test_size=0.2,
        random_state=42,
        stratify=corpus["label"].astype(int),
    )

    clf_vectorizer = TfidfVectorizer(max_features=25000, ngram_range=(1, 2), min_df=2, max_df=0.95)
    X_train_vec = clf_vectorizer.fit_transform(X_train)
    X_test_vec = clf_vectorizer.transform(X_test)

    clf = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    y_prob = clf.predict_proba(X_test_vec)[:, 1]

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    metrics = {
        "accuracy": float(report["accuracy"]),
        "precision_outlier": float(report["1"]["precision"]),
        "recall_outlier": float(report["1"]["recall"]),
        "f1_outlier": float(report["1"]["f1-score"]),
        "roc_auc": float(roc_auc_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else float("nan"),
    }

    print("\nClassifier metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    # Score all loaded text so the review CSV shows the model's decisions.
    print("\nScoring all text for review...")
    review = corpus.copy()
    review_matrix = clf_vectorizer.transform(review["text"])
    review["outlier_probability"] = clf.predict_proba(review_matrix)[:, 1]
    review["outlier_prediction"] = clf.predict(review_matrix)

    anomaly_vectorizer = None
    anomaly_model = None

    # Train the unsupervised detector only when the extra anomaly signal is wanted.
    if not args.no_anomaly_detector:
        req_text = req_df["text"].map(clean_text) if not req_df.empty else pd.Series(dtype=str)
        req_text = req_text[req_text.str.strip() != ""].drop_duplicates()
        if len(req_text) > 0:
            print("Training IsolationForest...")
            anomaly_vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=1, max_df=0.95)
            req_matrix = anomaly_vectorizer.fit_transform(req_text)
            anomaly_model = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
            anomaly_model.fit(req_matrix)

            anomaly_matrix = anomaly_vectorizer.transform(review["text"])
            review["anomaly_score"] = anomaly_model.decision_function(anomaly_matrix)
            review["anomaly_prediction"] = anomaly_model.predict(anomaly_matrix)
        else:
            review["anomaly_score"] = np.nan
            review["anomaly_prediction"] = np.nan
    else:
        review["anomaly_score"] = np.nan
        review["anomaly_prediction"] = np.nan

    # Mark rows that deserve review so the later outlier gate can filter them out.
    review["needs_review"] = (
        (review["outlier_probability"] >= 0.4)
        | (review["anomaly_prediction"] == -1)
        | (review["text"].str.len() < 12)
    )
    review = review.sort_values(["needs_review", "outlier_probability"], ascending=[False, False]).reset_index(drop=True)

    # Save the trained artifacts for the rest of the pipeline.
    os.makedirs(OUTLIER_MODEL_DIR, exist_ok=True)
    joblib.dump(clf_vectorizer, OUTLIER_VECTORIZER_PATH)
    joblib.dump(clf, OUTLIER_CLASSIFIER_PATH)
    joblib.dump(metrics, OUTLIER_METRICS_PATH)

    if anomaly_vectorizer is not None and anomaly_model is not None:
        joblib.dump(anomaly_vectorizer, OUTLIER_ANOMALY_VECTORIZER_PATH)
        joblib.dump(anomaly_model, OUTLIER_ANOMALY_MODEL_PATH)

    review.to_csv(OUTLIER_REVIEW_BASE_PATH, index=False)

    # Print the results so the stage has a clear starting point in the pipeline logs.
    print(f"\nSaved trained models in: {OUTLIER_MODEL_DIR}")
    print(f"Saved review CSV in: {OUTLIER_REVIEW_BASE_PATH}")
    print("\nTop review rows:")
    print(review[["text", "source", "label", "outlier_probability", "anomaly_score", "needs_review"]].head(10))


if __name__ == "__main__":
    main()