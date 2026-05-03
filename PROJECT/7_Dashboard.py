# ==========================================
# PIPELINE STEP 8: Streamlit Dashboard
# Objective: Provide an interactive interface for requirement classification,
# model inspection, and quick dataset exploration using the saved artifacts.
# ==========================================

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import scipy.sparse
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# ==========================================
# PAGE SETUP
# ==========================================

st.set_page_config(
    page_title="Software Requirements Classifier",
    page_icon="🧠",
    layout="wide"
)

st.title("Software Requirements Classification Dashboard")
st.caption("Functional vs Non-Functional requirement prediction using TF-IDF and Logistic Regression.")

# ==========================================
# PATHS AND ASSETS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "PROMISE-relabeled-NICE.csv"
TFIDF_MATRIX_PATH = BASE_DIR / "tfidf_matrix.npz"
TFIDF_LABELS_PATH = BASE_DIR / "tfidf_labels.npy"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"
MODEL_PATH = BASE_DIR / "requirement_classifier.pkl"

@st.cache_data
def load_dataset():
    # Load the cleaned dataset for exploration and batch prediction.
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_artifacts():
    # Load the saved model and vectorizer once to keep the dashboard fast.
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    tfidf_matrix = scipy.sparse.load_npz(TFIDF_MATRIX_PATH)
    tfidf_labels = np.load(TFIDF_LABELS_PATH)
    return model, vectorizer, tfidf_matrix, tfidf_labels

# ==========================================
# LOAD DATA
# ==========================================

try:
    PROMISE = load_dataset()
    model, vectorizer, tfidf_matrix, tfidf_labels = load_artifacts()
except Exception as error:
    st.error(f"Failed to load project files: {error}")
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("Dashboard Menu")
page_choice = st.sidebar.radio(
    "Choose a section",
    ["Overview", "Single Prediction", "Batch Prediction", "Model Insights"]
)

# ==========================================
# OVERVIEW PAGE
# ==========================================

if page_choice == "Overview":
    st.subheader("Project Overview")
    st.write(
        "This app lets you explore the dataset, test the classifier on new requirement text, "
        "and inspect the most predictive words and n-grams used by the model."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Requirements", f"{len(PROMISE):,}")
    col2.metric("Columns", f"{PROMISE.shape[1]:,}")
    col3.metric("TF-IDF Features", f"{tfidf_matrix.shape[1]:,}")

    st.markdown("### Class Distribution")
    class_counts = PROMISE["IsFunctional"].value_counts().sort_index()
    class_labels = ["Non-Functional", "Functional"]

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=class_labels, y=class_counts.values, ax=ax1, palette="Set2")
    ax1.set_xlabel("Class")
    ax1.set_ylabel("Count")
    ax1.set_title("Functional vs Non-Functional Requirements")
    st.pyplot(fig1)

    st.markdown("### Requirement Length")
    PROMISE["WordCount"] = PROMISE["RequirementText"].astype(str).apply(lambda text: len(text.split()))
    fig2, ax2 = plt.subplots(figsize=(9, 4))
    sns.histplot(PROMISE["WordCount"], bins=30, kde=True, color="steelblue", ax=ax2)
    ax2.set_xlabel("Word Count")
    ax2.set_ylabel("Frequency")
    ax2.set_title("Requirement Length Distribution")
    st.pyplot(fig2)

# ==========================================
# SINGLE PREDICTION PAGE
# ==========================================

elif page_choice == "Single Prediction":
    st.subheader("Predict a Requirement")
    st.write("Type any software requirement below and the model will classify it as Functional or Non-Functional.")

    sample_text = "The system shall allow users to reset their password using a secure email link."
    requirement_text = st.text_area("Requirement Text", value=sample_text, height=140)

    if st.button("Predict Requirement Type"):
        if requirement_text.strip() == "":
            st.warning("Please enter a requirement first.")
        else:
            transformed_text = vectorizer.transform([requirement_text])
            prediction = model.predict(transformed_text)[0]
            prediction_proba = model.predict_proba(transformed_text)[0]

            if prediction == 1:
                st.success(f"Prediction: Functional Requirement")
            else:
                st.info(f"Prediction: Non-Functional Requirement")

            st.write(f"Functional probability: {prediction_proba[1]:.4f}")
            st.write(f"Non-Functional probability: {prediction_proba[0]:.4f}")

# ==========================================
# BATCH PREDICTION PAGE
# ==========================================

elif page_choice == "Batch Prediction":
    st.subheader("Batch Prediction")
    st.write("Upload a CSV file with a RequirementText column to classify multiple requirements at once.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)

        if "RequirementText" not in input_df.columns:
            st.error("The uploaded file must contain a 'RequirementText' column.")
        else:
            transformed_matrix = vectorizer.transform(input_df["RequirementText"].astype(str))
            predictions = model.predict(transformed_matrix)

            prediction_labels = np.where(predictions == 1, "Functional", "Non-Functional")
            input_df["Prediction"] = prediction_labels

            st.success("Batch prediction complete.")
            st.dataframe(input_df.head(20), use_container_width=True)
            st.download_button(
                label="Download Predictions",
                data=input_df.to_csv(index=False).encode("utf-8"),
                file_name="requirement_predictions.csv",
                mime="text/csv"
            )

# ==========================================
# MODEL INSIGHTS PAGE
# ==========================================

else:
    st.subheader("Model Insights")
    st.write("This section shows evaluation results and the most important features used by the classifier.")

    # Recreate the train/test split so the evaluation is visible in the dashboard.
    X_train, X_test, y_train, y_test = train_test_split(
        tfidf_matrix,
        tfidf_labels,
        test_size=0.2,
        random_state=42
    )

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["Non-Functional", "Functional"])
    cm = confusion_matrix(y_test, y_pred)

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Accuracy", f"{accuracy * 100:.2f}%")
    metric_col2.metric("Test Samples", f"{len(y_test):,}")

    st.markdown("### Classification Report")
    st.text(report)

    st.markdown("### Confusion Matrix")
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Non-Functional", "Functional"],
        yticklabels=["Non-Functional", "Functional"],
        ax=ax3
    )
    ax3.set_xlabel("Predicted Label")
    ax3.set_ylabel("True Label")
    ax3.set_title("Confusion Matrix")
    st.pyplot(fig3)

    st.markdown("### Top Predictive Features")
    feature_names = vectorizer.get_feature_names_out()
    coefficients = model.coef_[0]
    importance = np.abs(coefficients)
    top_indices = np.argsort(importance)[-15:][::-1]

    top_features = pd.DataFrame({
        "Feature": feature_names[top_indices],
        "Importance": importance[top_indices]
    })

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_features, y="Feature", x="Importance", ax=ax4, color="steelblue")
    ax4.set_title("Top 15 Predictive Features")
    ax4.set_xlabel("Absolute Coefficient Value")
    ax4.set_ylabel("Feature")
    st.pyplot(fig4)

    st.dataframe(top_features, use_container_width=True)
