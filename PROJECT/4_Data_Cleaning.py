# ==========================================
# PIPELINE STEP 4: Data Cleaning & Preprocessing
# Objective: Standardize raw textual data by removing noise (punctuation, 
# stop words), tokenizing numerical metrics to <NUM>, and applying 
# lemmatization to prepare the text for feature extraction.
# ==========================================

import pandas as pd 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load the dataset
PROMISE = pd.read_csv('PROMISE-relabeled-NICE.csv')

#create a new column for the cleaned text
PROMISE['CleanedRequirementText'] = PROMISE['RequirementText']

#convert to lowercase for uniformity
PROMISE['CleanedRequirementText'] = PROMISE['RequirementText'].str.lower()

# 1. Remove punctuation (Using 'r' to prevent Python 3.12 syntax warnings)
PROMISE['CleanedRequirementText'] = PROMISE['CleanedRequirementText'].str.replace(r'[^\w\s]', '', regex=True)

# 2. Remove stop words
stop_words = set(stopwords.words('english'))
PROMISE['CleanedRequirementText'] = PROMISE['CleanedRequirementText'].apply(
    lambda x: ' '.join([word for word in word_tokenize(x) if word not in stop_words])
)

# 3. Replace numbers with <NUM> token instead of deleting them entirely
PROMISE['CleanedRequirementText'] = PROMISE['CleanedRequirementText'].str.replace(r'\d+', ' NUM ', regex=True)

# 4. Remove extra whitespace
PROMISE['CleanedRequirementText'] = PROMISE['CleanedRequirementText'].str.strip().str.replace(r'\s+', ' ', regex=True)

# 5. Lemmatization 
lemmatizer = WordNetLemmatizer()
PROMISE['CleanedRequirementText'] = PROMISE['CleanedRequirementText'].apply(
    lambda x: ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(x)])
)

# 6. Remove duplicates based on the CLEANED text
PROMISE.drop_duplicates(subset='CleanedRequirementText', inplace=True)

# 7. Remove rows where the cleaning process left the text completely empty
PROMISE = PROMISE[PROMISE['CleanedRequirementText'] != '']

# 8. Reset index after dropping rows
PROMISE.reset_index(drop=True, inplace=True)


# 10. Save the cleaned dataset
PROMISE.to_csv('PROMISE-relabeled-NICE.csv', index=False)
print("\nSuccess! Saved to PROMISE-relabeled-NICE.csv")

# SANITY CHECK: Print side-by-side comparison cleanly
print("\n--- PREPROCESSING COMPLETE: SIDE-BY-SIDE CHECK ---")
sample_df = PROMISE[['RequirementText', 'CleanedRequirementText']].sample(5, random_state=42)

for index, row in sample_df.iterrows():
    print(f"Row {index}:")
    print(f"  ORIGINAL: {row['RequirementText']}")
    print(f"  CLEANED : {row['CleanedRequirementText']}")
    print("-" * 80) # Adds a clean dividing line between examples