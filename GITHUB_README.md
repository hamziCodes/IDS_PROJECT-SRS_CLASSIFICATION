# Vertex IDS - Intelligent Requirement Classification System

**Vertex Intelligent Data Solutions** is an AI-powered system that automatically classifies software requirements into **Functional Requirements (FR)**, **Non-Functional Requirements (NFR)**, and identifies specific NFR types. The system combines academic research with a production-ready mobile application to bridge the gap between data science and real-world deployment.

## 🎯 What Does Vertex IDS Do?

Vertex IDS solves a critical problem in software engineering: **automatically understanding and organizing requirements**. Given a block of requirement text, the system:

1. **Identifies non-requirements** - Filters out irrelevant text using an outlier detection model
2. **Classifies requirements** - Determines if each requirement is Functional or Non-Functional
3. **Categorizes NFR types** - If Non-Functional, identifies the specific type (Security, Performance, Usability, etc.)
4. **Calculates confidence scores** - Provides confidence metrics for each prediction

### Example
```
Input: "The system shall encrypt all user data at rest with AES-256."

Output:
- Classification: Non-Functional Requirement
- NFR Type: Security (SE)
- Confidence: 0.94
```

---

## 📁 Project Structure

This repository contains everything needed to train, test, and deploy the Vertex IDS system:

```
IDS_PROJECT/
├── PROJECT/                    # Academic research & training pipeline
├── DATASETS/                   # Input data and training datasets
├── trained_models/             # Pre-trained model artifacts
├── vertex_app/                 # Production Flutter mobile app
└── README.md                   # This file
```

### Folder Overview

#### **1. `PROJECT/` - The Academic Research Pipeline**

This folder contains the complete machine learning pipeline that trains the classification models. It's organized as 6 independent stages that can be run sequentially.

**Why separate stages?**
- Each stage is small and focused on one task
- Easy to debug and modify individual components
- Can be run independently for testing
- Clear progression from raw data to trained models

**The 6 Pipeline Stages:**

| Stage | File | Purpose | Easy Explanation |
|-------|------|---------|------------------|
| **0** | `0_Outlier_Training.py` | Train the outlier detector | Teaches the model to recognize junk text so we can filter it out early |
| **1** | `1_Load_and_Merge.py` | Load and combine datasets | Gathers requirement datasets and combines them into one file |
| **2** | `2_Outlier_Gate.py` | Filter junk text | Removes obvious non-requirements using rules and the model from Stage 0 |
| **3** | `3_EDA.py` | Data exploration | Shows statistics about the cleaned data (how many FR vs NFR, text lengths, etc.) |
| **4** | `4_Data_Cleaning.py` | Clean requirement text | Normalizes text, removes duplicates, removes empty rows - prepares for training |
| **5** | `5_Feature_Engineering.py` | Convert text to numbers | Turns text into numerical vectors using TF-IDF so machines can understand it |
| **6** | `6_Model_Training_and_Export.py` | Train final models | Trains the FR/NFR classifier and the NFR type classifier, saves them |

**How They Work Together:**
```
Raw Data → Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Trained Models
```

Each stage reads output from the previous stage and writes output for the next stage. Running the full pipeline:

```bash
python PROJECT/RUN_PIPELINE_TRAINING.py
```

**Key Files in PROJECT/:**
- `pipeline_common.py` - Shared utilities (text cleaning, paths, dataset loading)
- `requirements.txt` - Python dependencies for training
- `app.py` - Demo Streamlit app that loads trained models and lets you test predictions interactively

#### **2. `DATASETS/` - Training Data**

Contains the requirement datasets used to train the models:

- **`PROMISE-relabeled-NICE.csv`** - The PROMISE software requirements dataset (real-world requirements)
- **`synthetic_NFR_augmentation.csv`** - Synthetic Non-Functional requirements generated for better NFR classification
- **`combined_stage*.csv`** - Intermediate files created during pipeline execution
- **`outlier_review*.csv`** - Outliers identified during the cleaning process

These datasets are fed through the 6-stage pipeline to create the trained models.

#### **3. `trained_models/` - Saved Model Artifacts**

After the pipeline runs, trained models are saved here for later use:

**`trained_models/FR_NFRTrained_models/`** - Main classifiers
- `model_fr_nfr.pkl` - The classifier that determines if a requirement is Functional or Non-Functional
- `model_nfr_types.pkl` - The classifier that determines which NFR type (Security, Performance, etc.)
- `vectorizer_combined.pkl` - The TF-IDF vectorizer that converts text to numbers
- `model_metadata.pkl` - Training metadata (model performance metrics, etc.)
- `nfr_types.npy` - List of NFR types the model recognizes

**`trained_models/outlierTrained_model/`** - Outlier detection
- `outlier_classifier.pkl` - Detects junk/non-requirement text
- `outlier_vectorizer.pkl` - Vectorizer for the outlier model

These files are loaded by both the Streamlit demo app and the Flutter production app.

#### **4. `vertex_app/` - Production Mobile Application**

This is the **production-ready Flutter application** that brings the trained models to end-users. It's much more than a simple demo - it adds significant features and bridges the gap between data scientists and actual users.

**Why a separate app?**
- Streamlit (app.py) is great for quick demos but limited for production
- Vertex App provides a professional, polished mobile interface
- Supports both Android and iOS
- Includes features like batch processing, history, PDF export, and sharing
- Uses a FastAPI backend that serves predictions over the network

**Key Features of Vertex App:**
- 📱 Native mobile experience (Android & iOS)
- 🔄 Batch processing - classify multiple requirements at once
- 💾 Local history - save and review past classifications
- 📥 Import/Export - CSV import and export
- 📄 PDF generation - Generate professional PDF reports
- 🔗 Share results - Share classifications with others
- 🎨 Beautiful UI - Modern, intuitive interface
- 🌐 Web support - Also runs on web browsers

**Architecture:**
```
Mobile App (Flutter) ↔ Backend API (FastAPI) ↔ Trained Models
```

The backend (`vertex_app/backend/`) loads the trained models and serves predictions via REST API, allowing the mobile app to work across networks and platforms.

---

## 🚀 Quick Start

### Option 1: Train Your Own Models (Full Pipeline)

```bash
# Install dependencies
pip install -r PROJECT/requirements.txt

# Run the complete training pipeline (stages 0-6)
python PROJECT/RUN_PIPELINE_TRAINING.py

# This creates trained models in trained_models/
```

### Option 2: Test with Streamlit Demo (Quick Test)

If you already have trained models:

```bash
# Install dependencies
pip install -r PROJECT/requirements.txt

# Run the Streamlit demo app
streamlit run PROJECT/app.py
```

The app opens in your browser. Type a requirement and see it classified in real-time.

### Option 3: Use the Production Flutter App

#### Backend API
```bash
cd vertex_app/backend

# Install dependencies
python -m pip install --user -r requirements.txt

# Start the API server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Flutter App
```bash
cd vertex_app

# Install Flutter dependencies
flutter pub get

# Run on Chrome (web)
flutter run -d chrome

# Run on Android emulator
flutter run -d emulator-5554

# Run on iOS simulator
flutter run -d "iPhone 15"
```

---

## 📊 How the System Works

### 1. **Training Phase** (PROJECT/ folder)

The 6-stage pipeline transforms raw requirement text into trained models:

```
Stage 0: Outlier Detection
└─ Train model to recognize junk text (greetings, personal intros, etc.)

Stage 1: Data Merging
└─ Combine PROMISE dataset + synthetic NFR dataset

Stage 2: Outlier Filtering
└─ Remove obvious non-requirements using rules + Stage 0 model

Stage 3: Data Analysis
└─ Generate statistics about the cleaned data

Stage 4: Text Cleaning
└─ Normalize text: lowercase, remove punctuation, lemmatize, remove stopwords

Stage 5: Feature Extraction
└─ Convert text to TF-IDF vectors (numerical representation)

Stage 6: Model Training
└─ Train 2 classifiers:
   a) FR vs NFR classifier
   b) NFR type classifier (13 types: Security, Performance, etc.)
```

### 2. **Inference Phase** (Runtime - App/API)

When a user types a requirement:

```
User Input
    ↓
Text Cleaning (same normalization as training)
    ↓
Vectorization (TF-IDF - convert to numbers)
    ↓
Outlier Check (Stage 0 model)
    ├─ If outlier: Show warning, offer force-classify
    └─ If not outlier: Continue
    ↓
FR/NFR Classification (Stage 6a model)
    ├─ If Functional: Show FR
    └─ If Non-Functional: Continue
    ↓
NFR Type Classification (Stage 6b model)
    └─ Identify which NFR type (Security, Performance, etc.)
    ↓
Display Results
    ├─ Classification confidence
    ├─ NFR types (if applicable)
    └─ Outlier probability
```

### 3. **NFR Types Recognized**

The system can classify Non-Functional Requirements into 13 categories:

| Code | Type | Example |
|------|------|---------|
| **SE** | Security | "The system shall encrypt all data at rest" |
| **PE** | Performance | "The system shall respond within 200ms" |
| **US** | Usability | "The interface shall be intuitive for new users" |
| **MN** | Maintainability | "Code shall have >80% unit test coverage" |
| **A** | Availability | "The system shall have 99.9% uptime" |
| **SC** | Scalability | "The system shall handle 1M concurrent users" |
| **FT** | Fault Tolerance | "The system shall recover from network failures" |
| **O** | Operability | "The system shall support Docker deployment" |
| **L** | Legal | "The system shall comply with GDPR" |
| **LF** | Look & Feel | "The interface shall use modern design patterns" |
| **PO** | Portability | "The app shall run on Android and iOS" |
| **OT** | Other | Other types of non-functional requirements |

---

## 📚 Dataset Details

### PROMISE Dataset
- **Source**: Real software requirements from real projects
- **Relabeling**: NICE annotations for FR vs NFR classification
- **Size**: Thousands of real-world requirements

### Synthetic NFR Augmentation
- **Purpose**: Improve NFR classification accuracy
- **Method**: Generated synthetic Non-Functional requirements to balance the dataset
- **Benefit**: Models learn better NFR patterns with more examples

### Data Pipeline
```
Raw CSV → Stage 1 (Merge) → Stage 2 (Filter) → Stage 4 (Clean) → Training
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│         Vertex IDS System               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   TRAINING PIPELINE (PROJECT/)   │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │ Stage 0: Outlier Training  │  │  │
│  │  │ Stage 1: Load & Merge      │  │  │
│  │  │ Stage 2: Outlier Gate      │  │  │
│  │  │ Stage 3: EDA               │  │  │
│  │  │ Stage 4: Data Cleaning     │  │  │
│  │  │ Stage 5: Feature Engineer  │  │  │
│  │  │ Stage 6: Model Training    │  │  │
│  │  └────────────────────────────┘  │  │
│  └──────────────────────────────────┘  │
│                    ↓                    │
│  ┌──────────────────────────────────┐  │
│  │   TRAINED MODELS (trained_models/)   │
│  │  ├─ FR/NFR Classifier            │  │
│  │  ├─ NFR Type Classifier          │  │
│  │  └─ Outlier Detector             │  │
│  └──────────────────────────────────┘  │
│                    ↓                    │
│  ┌──────────────────────────────────┐  │
│  │    DEMO APP (Streamlit)          │  │
│  │    Quick testing in browser      │  │
│  └──────────────────────────────────┘  │
│                    ↓                    │
│  ┌──────────────────────────────────┐  │
│  │   PRODUCTION STACK               │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │  FastAPI Backend           │  │  │
│  │  │  ↕ Loads trained models    │  │  │
│  │  │  ↕ Serves predictions      │  │  │
│  │  └────────────────────────────┘  │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │  Flutter Mobile App        │  │  │
│  │  │  ↕ Beautiful UI            │  │  │
│  │  │  ↕ Batch processing        │  │  │
│  │  │  ↕ History & Export        │  │  │
│  │  └────────────────────────────┘  │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🎓 Academic Pipeline Explained Simply

Think of the pipeline as a journey from raw messy data to a working AI model:

1. **Stage 0**: "Learn what junk looks like" - Train a model to identify irrelevant text
2. **Stage 1**: "Gather all the data" - Combine multiple datasets
3. **Stage 2**: "Remove the junk" - Filter out irrelevant entries
4. **Stage 3**: "Understand the data" - See what we have (balance, length, etc.)
5. **Stage 4**: "Clean up the text" - Standardize everything (remove punctuation, lowercase, etc.)
6. **Stage 5**: "Convert to numbers" - Turn text into vectors machines can understand
7. **Stage 6**: "Train the model" - Actually train the classifiers and save them

Result: Trained models ready for production!

---

## 🔄 Demo App vs Production App

| Feature | Streamlit Demo (`app.py`) | Flutter App (`vertex_app/`) |
|---------|---------------------------|---------------------------|
| **Purpose** | Quick testing & demonstration | Production deployment |
| **Interface** | Web browser (simple) | Native mobile (polished) |
| **Performance** | Good for testing | Optimized for production |
| **Batch Processing** | Not supported | ✅ Classify multiple at once |
| **History** | Not saved | ✅ View past classifications |
| **Export** | Simple copy-paste | ✅ PDF, CSV export |
| **Sharing** | Copy results | ✅ Share with others |
| **Platforms** | Web browsers | Android, iOS, Web |
| **Ideal For** | Dev/research | End-users, enterprises |

**Use Streamlit for:** Testing model changes, quick verification, debugging

**Use Flutter App for:** Real-world usage, client deployments, production environments

---

## 📦 Installation & Dependencies

### For Training Pipeline
```bash
pip install -r PROJECT/requirements.txt
```

Key packages:
- `scikit-learn` - ML models
- `pandas` - Data manipulation
- `nltk` - Text processing
- `numpy` - Numerical computing

### For Backend API
```bash
pip install -r vertex_app/backend/requirements.txt
```

Key packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- All packages from PROJECT/

### For Flutter App
```bash
# Install Flutter (one-time)
# https://flutter.dev/docs/get-started/install

cd vertex_app
flutter pub get  # Install dependencies
```

---

## 📋 File Structure Reference

```
PROJECT/
├── 0_Outlier_Training.py          ← Stage 0: Train outlier detector
├── 1_Load_and_Merge.py            ← Stage 1: Combine datasets
├── 2_Outlier_Gate.py              ← Stage 2: Filter junk
├── 3_EDA.py                       ← Stage 3: Data analysis
├── 4_Data_Cleaning.py             ← Stage 4: Clean text
├── 5_Feature_Engineering.py       ← Stage 5: Convert to vectors
├── 6_Model_Training_and_Export.py ← Stage 6: Train models
├── RUN_PIPELINE_TRAINING.py       ← Run all stages (0→6)
├── app.py                         ← Streamlit demo app
├── pipeline_common.py             ← Shared utilities
└── requirements.txt               ← Python dependencies

trained_models/
├── FR_NFRTrained_models/
│   ├── model_fr_nfr.pkl           ← FR/NFR classifier
│   ├── model_nfr_types.pkl        ← NFR type classifier
│   ├── vectorizer_combined.pkl    ← Text vectorizer
│   └── model_metadata.pkl         ← Model info
└── outlierTrained_model/
    ├── outlier_classifier.pkl     ← Outlier detector
    └── outlier_vectorizer.pkl     ← Outlier vectorizer

vertex_app/
├── backend/                       ← FastAPI backend
│   ├── app/main.py               ← API entrypoint
│   ├── app/model_loader.py       ← Load trained models
│   ├── app/predictor.py          ← Make predictions
│   ├── app/schemas.py            ← API request/response shapes
│   └── requirements.txt          ← Backend dependencies
└── lib/                          ← Flutter app code
    ├── main.dart                 ← App entry point
    ├── features/
    │   ├── chat/                 ← Classification feature
    │   ├── model/                ← Model info display
    │   ├── about/                ← About page
    │   └── splash/               ← Splash screen
    └── core/                     ← Shared utilities
        ├── services/             ← API client, export
        ├── widgets/              ← Reusable components
        └── config/               ← Configuration

DATASETS/
├── PROMISE-relabeled-NICE.csv                    ← Raw PROMISE data
├── synthetic_NFR_augmentation.csv                ← Synthetic NFRs
├── combined_stage1.csv                           ← After Stage 1
├── combined_stage2_filtered.csv                  ← After Stage 2
├── combined_stage4_cleaned.csv                   ← After Stage 4
└── outlier_review.csv                            ← Identified outliers
```

---

## 🧪 Testing

### Test the Pipeline
```bash
python PROJECT/RUN_PIPELINE_TRAINING.py
```

### Test Individual Stage
```bash
python PROJECT/4_Data_Cleaning.py  # Run just Stage 4
```

### Test the Demo App
```bash
streamlit run PROJECT/app.py
```
Then open http://localhost:8501 and type test requirements.

### Test Backend API
```bash
# Start backend
cd vertex_app/backend
python -m uvicorn app.main:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The system shall encrypt user data.", "force_classify": false}'
```

### Test Flutter App
```bash
cd vertex_app
flutter run -d chrome  # Web
# or
flutter run -d emulator-5554  # Android
```

---

## 🤝 Contributing

This is an academic research project. To extend it:

1. **Add new datasets**: Place in `DATASETS/`, update `pipeline_common.py` paths
2. **Modify pipeline**: Edit individual stages in `PROJECT/`, rerun pipeline
3. **Add app features**: Modify Flutter code in `vertex_app/lib/`
4. **Update backend**: Modify `vertex_app/backend/app/`

---

## 📄 License

This project is part of academic research. Please check the LICENSE file for usage terms.

---

## 👥 Authors & Contact

**Vertex Intelligent Data Solutions**

- **Email**: vertex11solution@gmail.com
- **Website**: https://vertex-devsolutions.vercel.app/
- **LinkedIn (Hamza)**: https://www.linkedin.com/in/hamzasultan-dev/
- **LinkedIn (Shahzaib)**: https://www.linkedin.com/in/shahzaib-farooq-/

---

## 🙏 Acknowledgments

- PROMISE dataset for providing real-world software requirements
- scikit-learn, Flutter, and FastAPI communities
- NLTK for NLP utilities

---

**Happy Classifying! 🚀**

For questions or issues, please reach out through the contact information above.
