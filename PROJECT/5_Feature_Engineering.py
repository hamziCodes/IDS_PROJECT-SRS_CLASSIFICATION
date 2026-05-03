# ==========================================
    # PIPELINE STEP 5: Feature Engineering & Selection
    # Objective: Translate cleaned English text into a mathematical matrix 
    # using TF-IDF. Cap the vocabulary at the 5000 most predictive features 
    # (n-grams) to prevent overfitting and handle dimensionality reduction natively.
    # ==========================================

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse
import joblib

#TF-IDF for meaningful words in the reviews
PROMISE = pd.read_csv('PROMISE-relabeled-NICE.csv')

#dropping empy rows 
PROMISE.dropna(subset=['CleanedRequirementText'], inplace=True)

#define vectorizer with 5k max features and n-grams (1,2) to capture single words and pairs of words
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))

#fit and transform the cleaned requirements to get the TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(PROMISE['CleanedRequirementText'])
tfidf_labels = PROMISE['IsFunctional'].values

#feature names extarted by the vectorizer
feature_names = vectorizer.get_feature_names_out()

#print matrix stats 
print(f'TF-IDF matrix shape: {tfidf_matrix.shape}')
print(f'Number of Unique Features: {tfidf_matrix.shape[1]}')
print("\n Features/Vocalbulary Sample:")
print(feature_names[200:215])  # Print a sample of feature names

#save the TF-IDF matrix and labels for later use
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

#save the sparse matrix and labels
scipy.sparse.save_npz('tfidf_matrix.npz', tfidf_matrix)
np.save('tfidf_labels.npy', tfidf_labels)
print("TF-IDF matrix and labels saved successfully.")