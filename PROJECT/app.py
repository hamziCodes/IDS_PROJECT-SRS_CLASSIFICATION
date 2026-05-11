# ==========================================================================================================
# STREAMLIT TESTING APPLICATION: INTERACTIVE REQUIREMENT CLASSIFICATION
# Purpose: Test FR/NFR classification and NFR type prediction on user input
# Usage: streamlit run app.py
# ==========================================================================================================

import streamlit as st
import joblib
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import re


# ==========================================================================================================
# PAGE CONFIGURATION & STYLING
# ==========================================================================================================

st.set_page_config(
    page_title="Requirement Classification Tester",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    /* Ensure outlier/prediction text remains readable in dark mode by forcing
       black text inside the warning box when the user prefers a dark color scheme.
       Light mode keeps the original styling. */
    @media (prefers-color-scheme: dark) {
        .warning-box h3 { color: #000 !important; }
    }
</style>
""", unsafe_allow_html=True)


# ==========================================================================================================
# LOAD MODELS & ARTIFACTS (Cached)
# ==========================================================================================================

@st.cache_resource
def load_models():
    """
    Load all trained models and vectorizer from trained_models folder
    What: Retrieve pre-trained models from disk
    How: Use joblib to deserialize saved model files from organized folder
    Why: Cache prevents reloading on every app interaction (improves performance); models stored in dedicated folder
    """
    import os
    try:
        # Models are located at workspace root under trained_models/FR_NFRTrained_models
        base = os.path.dirname(__file__)
        models_dir = os.path.abspath(os.path.join(base, '..', 'trained_models', 'FR_NFRTrained_models'))
        if not os.path.exists(models_dir):
            raise FileNotFoundError(f"Expected model directory not found: {models_dir}")
        
        model_fr_nfr = joblib.load(os.path.join(models_dir, 'model_fr_nfr.pkl'))
        model_nfr_types = joblib.load(os.path.join(models_dir, 'model_nfr_types.pkl'))
        vectorizer = joblib.load(os.path.join(models_dir, 'vectorizer_combined.pkl'))
        nfr_types = np.load(os.path.join(models_dir, 'nfr_types.npy'), allow_pickle=True).tolist()
        metadata = joblib.load(os.path.join(models_dir, 'model_metadata.pkl'))
        
        # Outlier artifacts live at workspace root under trained_models/outlierTrained_model
        outlier_dir = os.path.abspath(os.path.join(base, '..', 'trained_models', 'outlierTrained_model'))
        outlier_vectorizer = None
        outlier_classifier = None
        try:
            vec_path = os.path.join(outlier_dir, 'outlier_vectorizer.pkl')
            clf_path = os.path.join(outlier_dir, 'outlier_classifier.pkl')
            if os.path.exists(vec_path) and os.path.exists(clf_path):
                outlier_vectorizer = joblib.load(vec_path)
                outlier_classifier = joblib.load(clf_path)
        except Exception:
            outlier_vectorizer = None
            outlier_classifier = None

        return model_fr_nfr, model_nfr_types, vectorizer, nfr_types, metadata, outlier_vectorizer, outlier_classifier
    except Exception as e:
        st.error(f"Failed to load models: {e}")
        return None, None, None, None, None, None, None


# ==========================================================================================================
# TEXT PREPROCESSING (same as training)
# ==========================================================================================================

def preprocess_text(text):
    """
    Clean and preprocess input text using same pipeline as training
    What: Transform raw requirement text to clean format
    How: Apply lowercase, stop word removal, lemmatization (same as training)
    Why: Ensure consistency between training and inference data
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text)
    # Remove stop words
    text = ' '.join([w for w in word_tokenize(text) if w not in stop_words])
    # Replace numbers
    text = ' '.join([' NUM ' if w.isdigit() else w for w in text.split()])
    # Lemmatization
    text = ' '.join([lemmatizer.lemmatize(w) for w in word_tokenize(text)])
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text


def clean_for_outlier_model(text):
    if text is None:
        return ''
    value = str(text).lower().strip()
    if value == 'nan':
        return ''
    value = re.sub(r'https?://\S+|www\.\S+', ' ', value)
    value = re.sub(r'[^a-z0-9\s]', ' ', value)
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def basic_outlier_rule(text):
    if text is None:
        return True
    v = str(text).strip().lower()
    if v == '' or v == 'nan':
        return True
    if len(v.split()) < 3:
        return True
    patterns = [r'^my name is\b', r'^i am\b', r'^hello\b', r'^hi\b', r'\bcontact me\b']
    return any(re.search(p, v) for p in patterns)


# Load artifacts
model_fr_nfr, model_nfr_types, vectorizer, nfr_types, metadata, outlier_vectorizer, outlier_classifier = load_models()

if model_fr_nfr is None:
    st.error("❌ Models not found. Please ensure model files are in the current directory.")
    st.stop()

# ==========================================================================================================
# APPLICATION HEADER
# ==========================================================================================================

st.title("📋 Software Requirement Classification Tester")
st.markdown("""
**Interactive Testing Platform** for Functional/Non-Functional Requirement Classification
- Test requirement text against trained models
- Get instant predictions on FR/NFR classification and NFR types
- Understand model predictions through feature analysis
""")

# ==========================================================================================================
# SIDEBAR: APP INFORMATION & CONTROLS
# ==========================================================================================================

with st.sidebar:
    st.markdown("<h3 title='High-level info about loaded models and their performance'>📊 Model Information</h3>", unsafe_allow_html=True)
    st.markdown("### Model Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div title='Number of samples used to train the models'>Training Samples</div>", unsafe_allow_html=True)
        st.metric("ts", f"{metadata['n_train']:,}", label_visibility="collapsed")
        st.markdown("<div title='Number of samples used for testing'>Test Samples</div>", unsafe_allow_html=True)
        st.metric("test", f"{metadata['n_test']:,}", label_visibility="collapsed")
    with col2:
        st.markdown("<div title='Size of the TF-IDF vocabulary used by the models'>Vocabulary Size</div>", unsafe_allow_html=True)
        st.metric("vocab", f"{metadata['vocab_size']:,}", label_visibility="collapsed")
        st.markdown("<div title='Accuracy of FR/NFR classification model'>FR/NFR Accuracy</div>", unsafe_allow_html=True)
        st.metric("acc", f"{metadata['accuracy_fr_nfr']*100:.2f}%", label_visibility="collapsed")
    
    st.markdown("<h5 title='List of Non-Functional Requirement categories the model predicts'>### NFR Types Supported</h5>", unsafe_allow_html=True)
    for i, nfr in enumerate(nfr_types, 1):
        st.text(f"{i:2d}. {nfr}")
    
    st.markdown("---")
    st.markdown("<h5 title='Steps to use the application'>### Instructions</h5>", unsafe_allow_html=True)
    st.info("""
    1. Enter requirement text in the main area
    2. Click 'Classify Requirement' to get predictions
    3. View results: FR/NFR classification and NFR types
    4. Check confidence scores and model insights
    """)


# ==========================================================================================================
# MAIN: Single prediction
# ==========================================================================================================

# ==========================================================================================================
# MAIN CONTENT: SINGLE PREDICTION INTERFACE
# ==========================================================================================================

st.markdown("---")
st.markdown("<h4 title='Enter a single requirement and click classify to get FR/NFR and NFR-type predictions'>🔍 Single Requirement Classification</h4>", unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns([3, 1])
with col1:
    requirement_text = st.text_area(
        label="📝 Enter Requirement Text",
        placeholder="Paste or type a software requirement here...",
        height=120,
        help="Enter the requirement text you want to classify"
    )

with col2:
    st.markdown("")
    st.markdown("")
    classify_button = st.button("🎯 Classify Requirement", use_container_width=True, help="Click to classify the entered requirement (Functional vs Non-Functional)")

# Processing and Results Section
if classify_button and requirement_text.strip():
    with st.spinner("Processing requirement..."):
        # 0) Quick rule and model-based outlier check.
        is_rule_outlier = basic_outlier_rule(requirement_text)

        outlier_prob = None
        is_model_outlier = False
        if outlier_vectorizer is not None and outlier_classifier is not None:
            try:
                out_x = outlier_vectorizer.transform([clean_for_outlier_model(requirement_text)])
                outlier_prob = float(outlier_classifier.predict_proba(out_x)[0][1])
                is_model_outlier = outlier_prob >= 0.4
            except Exception as e:
                outlier_prob = None
                is_model_outlier = False

        is_outlier_final = is_rule_outlier or is_model_outlier

        # If flagged, show an outlier badge and allow the user to force classification.
        force_classify = False
        if is_outlier_final:
            st.markdown('---')
            if outlier_prob is not None:
                st.markdown(f"<div class='warning-box'><h3>⚠️ OUTLIER / IRRELEVANT (prob={outlier_prob:.2f})</h3></div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box"><h3>⚠️ OUTLIER / IRRELEVANT (rule-based)</h3></div>', unsafe_allow_html=True)
            force_classify = st.checkbox("Force FR/NFR classification despite outlier flag")

        # 1) If not forcing classification and flagged as outlier, skip FR/NFR prediction.
        if is_outlier_final and not force_classify:
            st.markdown("---")
            st.info("This input was flagged as 'Other/Irrelevant' and will not be classified into FR/NFR. Inspect the cleaned text below or force classification.")
            # Show processing preview
            st.markdown("---")
            st.markdown("<h5 title='Shows how the input text is cleaned and preprocessed'>📝 Text Processing Preview</h5>", unsafe_allow_html=True)
            with st.expander("View Original vs Cleaned Text"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original Text:**")
                    st.text(requirement_text)
                with col2:
                    st.markdown("**Cleaned Text (for Vectorization):**")
                    st.text(preprocess_text(requirement_text))
        else:
            # 2) Proceed with normal preprocessing and classification
            cleaned_text = preprocess_text(requirement_text)
            text_tfidf = vectorizer.transform([cleaned_text])
            fr_nfr_pred = model_fr_nfr.predict(text_tfidf)[0]
            fr_nfr_proba = model_fr_nfr.predict_proba(text_tfidf)[0]
            nfr_type_preds = model_nfr_types.predict(text_tfidf)[0]

            # Display Results
            st.markdown("---")
            st.markdown("<h4 title='Classification model predictions and confidence scores'>✅ Classification Results</h4>", unsafe_allow_html=True)
        
        # If the input was flagged as outlier and the user did not force classification,
        # we already showed a preview above and should not attempt to display classification results.
        if not (is_outlier_final and not force_classify):
            # Main Classification Result
            result_col1, result_col2, result_col3 = st.columns([2, 1, 1])

            with result_col1:
                st.markdown("### Primary Classification")
                if fr_nfr_pred == 1:
                    st.markdown('<div class="success-box"><h3>🟢 FUNCTIONAL REQUIREMENT (FR)</h3></div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-box"><h3>🟡 NON-FUNCTIONAL REQUIREMENT (NFR)</h3></div>', 
                               unsafe_allow_html=True)

            with result_col2:
                st.markdown("<div title='Confidence score for Functional Requirement classification'>### FR Confidence</div>", unsafe_allow_html=True)
                st.metric("", f"{fr_nfr_proba[1]*100:.1f}%")

            with result_col3:
                st.markdown("<div title='Confidence score for Non-Functional Requirement classification'>### NFR Confidence</div>", unsafe_allow_html=True)
                st.metric("", f"{fr_nfr_proba[0]*100:.1f}%")

            # NFR Type Prediction (if NFR)
            if fr_nfr_pred == 0:
                st.markdown("---")
                st.markdown("<h4 title='Specific Non-Functional Requirement categories detected'>🏷️ Non-Functional Requirement Types Detected</h4>", unsafe_allow_html=True)

                detected_types = nfr_type_preds == 1

                if detected_types.any():
                    col1, col2 = st.columns(2)
                    for i, (nfr_type, detected) in enumerate(zip(nfr_types, nfr_type_preds)):
                        with col1 if i % 2 == 0 else col2:
                            if detected:
                                st.success(f"✓ {nfr_type}")
                            else:
                                st.caption(f"✗ {nfr_type}")
                else:
                    st.info("⚠️ No specific NFR types detected for this requirement")

            # Text Preprocessing Preview
            st.markdown("---")
            st.markdown("<h5 title='Shows how the input text is cleaned and preprocessed'>📝 Text Processing Preview</h5>", unsafe_allow_html=True)
            with st.expander("View Original vs Cleaned Text"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original Text:**")
                    st.text(requirement_text)
                with col2:
                    st.markdown("**Cleaned Text (for Vectorization):**")
                    st.text(cleaned_text)

elif classify_button and not requirement_text.strip():
    st.warning("⚠️ Please enter a requirement text before classifying.")


# ==========================================================================================================
# EXAMPLE REQUIREMENTS SECTION
# ==========================================================================================================

st.markdown("---")
st.markdown("<h4 title='Pre-written requirement examples you can test'>💡 Example Requirements to Test</h4>", unsafe_allow_html=True)

examples = {
    "Functional": [
        "The system shall calculate the total invoice amount based on line items.",
        "Users must be able to login with username and password.",
        "The application shall generate monthly reports."
    ],
    "Performance (NFR)": [
        "The system response time shall not exceed 2 seconds.",
        "Database queries must complete within 500ms.",
        "The application shall handle 10,000 concurrent users."
    ],
    "Security (NFR)": [
        "All data transmissions shall be encrypted using AES-256.",
        "The system shall validate user input against SQL injection attacks.",
        "Passwords shall be at least 12 characters long."
    ],
    "Usability (NFR)": [
        "The interface shall be intuitive and require minimal training.",
        "All buttons shall be clearly labeled.",
        "The application shall support multiple languages."
    ]
}

for category, examples_list in examples.items():
    with st.expander(f"📌 {category} Examples"):
        for j, example in enumerate(examples_list, 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.caption(f"{j}. {example}")
            with col2:
                if st.button("🔍 Test", key=f"btn_{category}_{j}"):
                    st.session_state.selected_example = example

# If user selected an example, display it
if "selected_example" in st.session_state:
    with st.container():
        st.info(f"Selected: {st.session_state.selected_example}")

# ==========================================================================================================
# FOOTER & INFORMATION
# ==========================================================================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div title='Total number of unique words in the model vocabulary'>**📊 Total Features (Vocabulary):** {:,}</div>".format(metadata['vocab_size']), unsafe_allow_html=True)
with col2:
    st.markdown("<div title='Number of requirements used in training'>**🎓 Training Data:** {:,} requirements</div>".format(metadata['n_train']), unsafe_allow_html=True)
with col3:
    st.markdown("<div title='Overall accuracy of the FR/NFR classification model'>**✅ Model Accuracy:** {:.2f}%</div>".format(metadata['accuracy_fr_nfr']*100), unsafe_allow_html=True)

st.caption("Powered by: Logistic Regression + TF-IDF | Multi-Label Classification for NFR Types")
