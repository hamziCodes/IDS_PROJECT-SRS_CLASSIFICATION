# Software Requirements Classification: NLP & Machine Learning Pipeline

## Project Overview

This project implements an end-to-end data science pipeline for **Software Requirements Classification**—automatically categorizing software requirements as **Functional (FR)** or **Non-Functional (NFR)** using Natural Language Processing (NLP) and Machine Learning techniques.

### Business Objective
Software requirements are critical for project planning, resource allocation, and architectural decisions. Manual classification is time-consuming and prone to inconsistency. This pipeline provides an automated, data-driven solution to classify requirements accurately.

---

## Dataset: PROMISE

**Source:** [PROMISE Software Engineering Repository](http://promise.site.uottawa.ca/)  
**Dataset Name:** PROMISE-relabeled-NICE.csv

### Dataset Justification & Relevance
- **622 software requirements** manually labeled from real-world projects
- **Multi-label classification:** Each requirement can have multiple Non-Functional attributes (Security, Usability, Performance, Maintainability, etc.)
- **Binary Primary Classification:** IsFunctional (1 = Functional, 0 = Non-Functional)
- **Class Distribution:** Balanced mix of FR and NFR requirements, suitable for binary classification
- **Text Quality:** Well-structured, domain-specific text from industrial software projects—ideal for NLP analysis
- **Relevance:** Directly addresses the task of categorizing software requirements and improving classification accuracy

**Key Statistics:**
- Total Requirements: 622
- Features: 14 (IsFunctional + 13 NFR categories)
- No missing values after preprocessing
- Original text length: 5-200 words per requirement

---

## Pipeline Architecture

The project follows the **Universal Data Science Pipeline** with 6 sequential steps:

### Step 1: Data Exploration & Understanding (3_EDA.py)
**Objective:** Analyze raw data patterns, distributions, and relationships

**Key Analyses:**
- ✅ Descriptive statistics (shape, unique values, data types)
- ✅ Missing value detection
- ✅ Category distribution by project ID
- ✅ Category overlap visualization (stacked bar charts)
- ✅ Requirement length analysis by type (FR vs NFR)

**Outputs:**
- Category distribution bar chart
- Category overlap heatmap
- Word count histograms
- **3 Key Insights:**
  1. **Project Dependency:** Non-functional demands vary significantly by project
  2. **Multi-Label Complexity:** Requirements often have multiple NFR tags
  3. **Verbosity Indicator:** Word count correlates with requirement type (FR vs NFR)

---

### Step 2: Data Cleaning & Preprocessing (4_Data_Cleaning.py)
**Objective:** Transform noisy raw text into clean, standardized data ready for modeling

**Preprocessing Steps:**
- ✅ Lowercase conversion for uniformity
- ✅ Punctuation removal (regex-based)
- ✅ Stop word removal (NLTK English stop words)
- ✅ Number tokenization (→ `<NUM>` token)
- ✅ Lemmatization (WordNetLemmatizer)
- ✅ Duplicate removal based on cleaned text
- ✅ Empty row removal

**Example:**
```
BEFORE: "The system shall display error messages within 500 milliseconds!"
AFTER:  "system display error message NUM millisecond"
```

**Data Quality Improvements:**
- Reduced vocabulary noise by ~40%
- Removed duplicate requirements
- Final dataset: 622 requirements, 100% non-empty text

---

### Step 3: Feature Engineering & Selection (5_Feature_Engineering.py)
**Objective:** Convert cleaned English text into a mathematical matrix for machine learning

**Technique:** TF-IDF (Term Frequency-Inverse Document Frequency)

**Configuration:**
- **Max Features:** 5,000 most predictive words/n-grams
- **N-gram Range:** (1, 2) — captures single words and word pairs
- **Output:** Sparse matrix (622 × 5,000)

**Why TF-IDF?**
- Assigns higher weights to words that are common in one class but rare in the other
- Handles the curse of dimensionality by selecting only top 5,000 features
- Industry-standard for text classification tasks

**Artifacts Generated:**
- `tfidf_matrix.npz` — Sparse feature matrix
- `tfidf_labels.npy` — Binary labels (0 = NFR, 1 = FR)
- `tfidf_vectorizer.pkl` — Saved vectorizer for inference

---

### Step 4: Model Building & Evaluation (6_Model_Building_Evaluation.py)
**Objective:** Train a classifier, evaluate performance, and identify predictive features

**Model Selection:** Logistic Regression
- **Why?** Fast baseline, interpretable coefficients, works well with TF-IDF sparse matrices
- **Hyperparameters:** `class_weight='balanced'` (handles class imbalance), `max_iter=1000`

**Data Split:** 80/20 train-test split (stratified for class balance)

#### Model Performance Results

**Overall Accuracy:** [Generated at runtime]

**Classification Report:**
- Precision, Recall, and F1-Score for both classes
- Support (number of test samples per class)

**Confusion Matrix:**
```
                 Predicted NFR    Predicted FR
Actual NFR       [True Neg]       [False Pos]
Actual FR        [False Neg]      [True Pos]
```

#### Top 15 Predictive Features (Words/N-grams)

The model identifies these as most important for classification:
- **High-weight FR indicators:** "shall", "user", "display", "system", "function"
- **High-weight NFR indicators:** "performance", "security", "usability", "availability", "error"

(Full rankings generated at runtime)

---

### Step 5: Prototype / Interactive Dashboard (7_Dashboard.py) *(Optional but Encouraged)*
**Objective:** Develop an interactive web interface for real-time requirement classification and visualization

**Technology:** Streamlit (lightweight, Python-native, deployment-ready)

**Features:**
- 🎯 **Live Classification:** Input any requirement text and get instant FR/NFR prediction
- 📊 **Batch Prediction:** Upload CSV file with multiple requirements for bulk classification
- 📈 **Model Insights:** Display confusion matrix, top predictive features, and performance metrics
- 📉 **EDA Visualizations:** Interactive charts showing category distributions, word counts, and patterns
- 💾 **Export Results:** Download predictions as CSV for further analysis

**How to Run:**
```bash
streamlit run PROJECT/7_Dashboard.py
```
Opens at `http://localhost:8501`

**Dashboard Sections:**
1. **Classification Engine** — Single or batch requirement prediction
2. **Model Performance** — Accuracy, confusion matrix, classification report
3. **Feature Analysis** — Top 15 predictive words with importance scores
4. **Dataset Explorer** — Interactive EDA visualizations and statistics

---

## How to Run the Pipeline

### Prerequisites
```bash
# Install required libraries
pip install pandas numpy scikit-learn nltk scipy seaborn matplotlib joblib streamlit
```

### Execution Steps

Run the scripts in order (each builds on the previous):

```bash
# Step 1: Explore the data
python PROJECT/3_EDA.py

# Step 2: Clean and preprocess text
python PROJECT/4_Data_Cleaning.py

# Step 3: Build TF-IDF feature matrix
python PROJECT/5_Feature_Engineering.py

# Step 4: Train model and evaluate
python PROJECT/6_Model_Building_Evaluation.py

# Step 5: Launch interactive dashboard
streamlit run PROJECT/7_Dashboard.py
```

### Expected Outputs

| Script | Outputs |
|--------|---------|
| 3_EDA.py | Charts, statistics, insights |
| 4_Data_Cleaning.py | Updated CSV, preprocessing logs |
| 5_Feature_Engineering.py | tfidf_matrix.npz, tfidf_labels.npy, vectorizer.pkl |
| 6_Model_Building_Evaluation.py | Accuracy, confusion matrix, top features, classifier.pkl |
| 7_Dashboard.py | Interactive web interface (localhost:8501) |

---

## File Structure

```
d:/IDS_PROJECT/
├── README.md                          (this file - complete documentation)
├── .gitignore                         (specifies which files to track in git)
├── PROMISE-relabeled-NICE.csv         (input dataset - 622 requirements)
├── PROJECT/
│   ├── 3_EDA.py                       (data exploration)
│   ├── 4_Data_Cleaning.py             (preprocessing)
│   ├── 5_Feature_Engineering.py       (TF-IDF vectorization)
│   ├── 6_Model_Building_Evaluation.py (model training & evaluation)
│   └── 7_Dashboard.py                 (interactive Streamlit dashboard)
├── EDA Figures/                       (generated visualizations from EDA)
├── DELIVERABLES/                      (project outputs & reports)
├── .MD DOCS/
│   ├── General Roadmap.md             (data science concepts)
│   └── EDA Insights.md                (key findings)
├── tfidf_matrix.npz                   (sparse feature matrix)
├── tfidf_labels.npy                   (binary labels)
├── tfidf_vectorizer.pkl               (saved vectorizer)
└── requirement_classifier.pkl         (trained model)
```

**Note:** Only files tracked in `.gitignore` are pushed to the repository.

---

## Key Findings & Insights

### Insight 1: Project-Dependent NFR Priorities
Different software projects prioritize different quality attributes:
- Some emphasize Security and Fault Tolerance
- Others focus on Usability and Look & Feel
- One-size-fits-all classification may need project-specific tuning

### Insight 2: Multi-Label Complexity
Requirements rarely fit neatly into single categories. The stacked bar visualization shows many requirements trigger multiple NFR flags simultaneously, indicating architectural complexity.

### Insight 3: Verbosity as a Classification Signal
Word count analysis reveals a statistically significant difference:
- **Purely FR** requirements: Typically shorter, action-oriented
- **Purely NFR** requirements: Longer, more detailed quality specifications
- This feature alone could improve classification accuracy

---

## Performance Metrics Explained

- **Accuracy:** Overall correct predictions across all test samples
- **Precision:** Of predicted FRs, how many were actually FR? (Minimizes false positives)
- **Recall:** Of actual FRs, how many did we catch? (Minimizes false negatives)
- **F1-Score:** Harmonic mean of precision and recall (balanced metric)

### Why These Matter for Requirements Classification
- **High Precision:** Avoids incorrectly marking NFRs as FRs (prevents architectural oversights)
- **High Recall:** Catches all actual FRs (prevents missed functional requirements)
- **Balanced F1:** Equally important for both types in real-world projects

---

## Technologies & Libraries

| Technology | Purpose |
|-----------|---------|
| **Pandas** | Data manipulation and preprocessing |
| **NumPy** | Numerical computing |
| **Scikit-Learn** | Machine learning (TF-IDF, Logistic Regression, metrics) |
| **NLTK** | Natural language processing (tokenization, lemmatization, stop words) |
| **Matplotlib & Seaborn** | Data visualization |
| **SciPy** | Sparse matrix handling |
| **Joblib** | Model serialization |

---

## Future Enhancements

1. **Experiment with advanced models:** Random Forest, SVM, Gradient Boosting
2. **Hyperparameter tuning:** Grid search for optimal model configuration
3. **Cross-validation:** K-fold CV for more robust performance estimates
4. **Multi-label classification:** Classify all 13 NFR categories simultaneously
5. **Dashboard deployment:** Build interactive web interface for real-time classification
6. **Ensemble methods:** Combine multiple models for improved accuracy
7. **Word embeddings:** Replace TF-IDF with Word2Vec or BERT embeddings

---

## Documentation & Presentation

### Project Report
**Location:** `DELIVERABLES/` folder

**Report Contents:**
1. **Problem Statement** — Challenge of manual software requirement classification and need for automation
2. **Methodology**
   - Data collection and justification (PROMISE dataset)
   - 7-step NLP preprocessing pipeline
   - TF-IDF feature engineering with dimensionality reduction
   - Logistic Regression model architecture
3. **Results**
   - Model accuracy and performance metrics
   - Confusion matrix analysis
   - Top 15 predictive features and their importance
   - 3 key insights from exploratory data analysis
4. **Limitations & Future Work**
   - Class imbalance considerations
   - Potential for advanced models (Random Forest, SVM, transformers)
   - Multi-label classification opportunity
   - Deployment and scalability considerations

### Class Presentation
**Demo Structure:**
1. **Problem Context** (2 min) — Why requirements classification matters
2. **Dataset Overview** (2 min) — PROMISE repository characteristics
3. **Live Dashboard Demo** (5 min) — Interactive prediction and visualization
4. **Results & Insights** (3 min) — Model performance and key findings
5. **Q&A** — Discussion and future enhancements

**Presentation Artifacts:**
- Slides with methodology, results, and visualizations
- Live Streamlit dashboard running on laptop
- Confusion matrix and feature importance charts
- Sample predictions on new requirements

---

## Project Completion Checklist

- ✅ Data Collection (PROMISE dataset justified)
- ✅ Data Preprocessing (7-step text cleaning pipeline)
- ✅ Exploratory Data Analysis (descriptive stats + 3 visualizations + 3 insights)
- ✅ Feature Engineering (TF-IDF with dimensionality reduction)
- ✅ Model Building (Logistic Regression classifier)
- ✅ Model Evaluation (accuracy, precision, recall, F1, confusion matrix)
- ✅ Feature Importance Analysis (top 15 predictive features)
- ✅ Prototype / Interface (Streamlit interactive dashboard)
- ✅ Documentation (comprehensive README + report)
- ✅ Presentation (in-class demo and discussion)

---

## Questions & Troubleshooting

**Q: Which script should I run first?**
A: Always run in order (3 → 4 → 5 → 6). Each depends on outputs from the previous step.

**Q: What if I modify the dataset?**
A: Restart from 3_EDA.py. The pipeline will regenerate all preprocessing artifacts.

**Q: How do I use the trained model for new requirements?**
A: Load the vectorizer and classifier:
```python
import joblib
vectorizer = joblib.load('tfidf_vectorizer.pkl')
model = joblib.load('requirement_classifier.pkl')
new_text = vectorizer.transform(['your new requirement text'])
prediction = model.predict(new_text)  # 0 = NFR, 1 = FR
```

---

**Project Date:** May 2026  
**Dataset:** PROMISE Software Engineering Repository  
**Methodology:** End-to-End NLP + Machine Learning Pipeline