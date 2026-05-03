# ==========================================
# PIPELINE STEP 3: Data Understanding & Exploration (EDA)
# Objective: Analyze the PROMISE dataset to discover underlying patterns, 
# check category distributions, and compare word counts between 
# Functional and Non-Functional requirements.
# ==========================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#importing the dataset
PROMISE = pd.read_csv('PROMISE-relabeled-NICE.csv')

#checking the shape of the dataset (rows, columns)
print("Shape: \n", PROMISE.shape)

#now we see the columns and the dtypes of the dataset
print("Info: \n", PROMISE.info())

#see unique values in each column to understand the data better
print("Unique values: \n", PROMISE.nunique())

#checking for missing values
missing_vals = PROMISE.isnull().sum()
print("Missing values in each column:")
print(missing_vals)

#plotting categories on bar graph to see  the distribution of the data
category_cols = ["IsFunctional" ,"IsQuality","Availability (A)","Fault Tolerance (FT)","Legal (L)","Look & Feel (LF)",
                 "Maintainability (MN)","Operability (O)","Performance (PE)","Portability (PO)","Scalability (SC)",
                 "Security (SE)","Usability (US)","Other (OT)"]
category_counts = PROMISE[category_cols].sum() #counting the number of occurrences of each category
plt.figure(figsize=(12, 6), layout='tight')
category_counts.plot(kind='bar')
plt.title('Distribution of Categories in PROMISE Dataset')
plt.xlabel('Categories')
plt.ylabel('Count')
plt.show()

#plotting common categories based on projectID
projects = ["ProjectID"]
for index in projects:
    project_data = PROMISE.groupby(index)[category_cols].sum()
    project_data.plot(kind='bar', stacked=True, figsize=(12, 6), layout='tight')
    plt.title(f'Category Distribution by {index}')
    plt.xlabel(index)
    plt.ylabel('Count')
    plt.legend(loc='upper right')
    plt.show()
#print the sum of each category for each projectID
project_category_sum = PROMISE.groupby("ProjectID")[category_cols].sum()
print(project_category_sum) 


# 1. Select calculated rows
PROMISE['CategoryCount'] = PROMISE[category_cols].sum(axis=1)

# 2. Create a simplesample and complex sample comprising of FR vs NFR(includes eveyrthing except FR)
complex_samples = PROMISE.nlargest(6, 'CategoryCount')
simple_samples = PROMISE[PROMISE["IsFunctional"] == 1].sample(6, random_state=42)

# 3. combine them for a 12 row plotting
plot_samples =pd.concat([complex_samples, simple_samples])

# 4. convert to int to remove boolean error and get first 50 string to plot on graph for readability
category_data = plot_samples[category_cols].astype(int)
category_data.index = plot_samples['RequirementText'].str[:50] + "..."

# 5. Re-plot with an explicit stacked parameter
plt.figure(figsize=(14, 8))
category_data.plot(kind='barh', stacked=True, colormap='tab20', ax=plt.gca())

plt.title('Category Overlap for Requirements')
plt.xlabel('Number of Labels')
plt.legend()
plt.tight_layout()
plt.show()

# 1. Calculate Word Count first 
PROMISE['WordCount'] = PROMISE['RequirementText'].apply(lambda x: len(str(x).split()))

# 2. Define all the NFR columns (excluding IsFunctional)
nfr_cols = [
    "IsQuality", "Availability (A)", "Fault Tolerance (FT)", "Legal (L)", 
    "Look & Feel (LF)", "Maintainability (MN)", "Operability (O)", 
    "Performance (PE)", "Portability (PO)", "Scalability (SC)", 
    "Security (SE)", "Usability (US)", "Other (OT)"
]

# 3. Create the 'HasNFR' master flag. 
# sum(axis=1) adds up the row. If the sum is > 0, it means at least one NFR is present.
PROMISE['HasNFR'] = (PROMISE[nfr_cols].sum(axis=1) > 0)

# 4. categorize
def categorize_req_robust(row):
    # Purely FR: IsFunctional is 1 AND HasNFR is 0
    if row['IsFunctional'] == 1 and row['HasNFR'] == 0:
        return 'Purely FR'
    
    # Purely NFR: IsFunctional is 0 (Meaning all tags must be NFRs)
    elif row['IsFunctional'] == 0:
        return 'Purely NFR'
    
    # Mixed: IsFunctional is 1 AND at least one NFR tag is present
    elif row['IsFunctional'] == 1 and row['HasNFR'] == 1:
        return 'Mixed (FR + NFR)'
    
    else:
        return 'Unknown'

# Create the new category column
PROMISE['ReqType'] = PROMISE.apply(categorize_req_robust, axis=1)

# 5. Calculate and print the averages for your report
avg_words = PROMISE.groupby('ReqType')['WordCount'].mean()

print("\n--- Word Count Averages (Robust Logic) ---")
print(f"Word count when purely FR = {avg_words.get('Purely FR', 0):.2f} words")
print(f"Word count when purely NFR = {avg_words.get('Purely NFR', 0):.2f} words")
print(f"Word count when Mixed (FR + NFR) = {avg_words.get('Mixed (FR + NFR)', 0):.2f} words")
print("------------------------------------------\n")

# 6. Plot the Histogram with the 3 accurate categories
plt.figure(figsize=(12, 6))

sns.histplot(data=PROMISE, x='WordCount', hue='ReqType', 
             bins=40, kde=True, palette='Set2')

plt.title('Requirement Lengths: Pure FR vs. Pure NFR vs. Mixed')
plt.xlabel('Number of Words in Requirement')
plt.ylabel('Frequency (Number of Requirements)')
plt.show()

# 7. A simple Bar Chart to clearly show the averages side-by-side
plt.figure(figsize=(8, 5))
sns.barplot(data=PROMISE, x='ReqType', y='WordCount', errorbar=None, palette='Set2')
plt.title('Average Word Count by Requirement Type')
plt.xlabel('Requirement Type')
plt.ylabel('Average Word Count')
plt.show()