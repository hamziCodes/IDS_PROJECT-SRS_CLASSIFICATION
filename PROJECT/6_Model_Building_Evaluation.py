# ==========================================
# PIPELINE STEP 6 & 7: Model Building & Evaluation
# Objective: Load the TF-IDF feature matrix, split the data to prevent 
# overfitting, train a Logistic Regression classifier, evaluate its 
# performance on unseen data, and export the trained model.
# ==========================================

import pandas as pd
import numpy as np
import scipy.sparse
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load the TF-IDF matrix and labels
tfidf_matrix = scipy.sparse.load_npz('tfidf_matrix.npz')
tfidf_labels = np.load('tfidf_labels.npy')

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(tfidf_matrix, tfidf_labels, test_size=0.2, random_state=42)
#what is stratify=y_labels

#initilalise nd train the classifier
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

#evaluate the model on the test set
print("\n--- MODEL PERFORMANCE ---")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Overall Accuracy: {accuracy * 100:.2f}%\n")

print("Detailed Classification Report:")
# Target names make the report easier to read (0 = Non-Functional, 1 = Functional)
print(classification_report(y_test, y_pred, target_names=['Non-Functional', 'Functional']))

# CONFUSION MATRIX VISUALIZATION
# Objective: Visualize true positives, true negatives, false positives, 
# and false negatives to understand where the model is making mistakes.

cm = confusion_matrix(y_test, y_pred)

# Create a heatmap visualization of the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Non-Functional', 'Functional'],
            yticklabels=['Non-Functional', 'Functional'],
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix: Requirement Classification Performance')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.show()

print("\n--- CONFUSION MATRIX BREAKDOWN ---")
tn, fp, fn, tp = cm.ravel()
print(f"True Negatives (TN):  {tn}")
print(f"False Positives (FP): {fp}")
print(f"False Negatives (FN): {fn}")
print(f"True Positives (TP):  {tp}")

# FEATURE IMPORTANCE ANALYSIS
# Objective: Extract the top 10-15 most predictive features (words/n-grams) 
# that the logistic regression model uses to classify requirements.

# Load the vectorizer to retrieve feature names
vectorizer = joblib.load('tfidf_vectorizer.pkl')
feature_names = vectorizer.get_feature_names_out()

# Extract model coefficients and sort by absolute importance
coefficients = model.coef_[0]
feature_importance = np.abs(coefficients)

# Get indices of top 15 most important features
top_feature_indices = np.argsort(feature_importance)[-15:][::-1]  # Reverse to get descending order
top_features = feature_names[top_feature_indices]
top_importance = feature_importance[top_feature_indices]

print("\n--- TOP 15 MOST PREDICTIVE FEATURES (Words/N-grams) ---")
for idx, (feature, importance) in enumerate(zip(top_features, top_importance), 1):
    print(f"{idx:2d}. '{feature}' (importance score: {importance:.4f})")

# Visualize feature importance
plt.figure(figsize=(10, 8))
plt.barh(range(len(top_features)), top_importance, color='steelblue')
plt.yticks(range(len(top_features)), top_features)
plt.xlabel('Absolute Coefficient Value (Importance Score)')
plt.title('Top 15 Most Predictive Features for Requirement Classification')
plt.gca().invert_yaxis()  # Highest importance at the top
plt.tight_layout()
plt.show()

#export trained model for deployment
print("\n--- SAVING TRAINED MODEL ---")
joblib.dump(model, 'requirement_classifier.pkl')
print("Success! Saved requirement_classifier.pkl.")
print("All backend assets are now ready for the dashboard deployment.")