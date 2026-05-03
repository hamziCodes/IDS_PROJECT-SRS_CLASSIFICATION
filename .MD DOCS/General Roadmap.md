EDA ROADMAP: A Step-by-Step Guide to Exploratory Data Analysis for Text Data
How you can decide this for future projects:

Whenever you start a project, ask yourself:

Is my data balanced? (Use Bar Charts)

Is there a pattern in how much data I have? (Use Histograms/Box Plots)

What are the "Key Players" (words/values) in my data? (Use Word Clouds/Frequency Plots)

Are there relationships between variables? (Use Correlation Heatmaps—though less common for pure text).


Summary of your EDA Checklist:

|If you want to know...|Use this Visual...|
|-|-|
|"Is my model going to be biased?"|Bar Chart of Classes|
|"Did I clean the text correctly?"|Word Cloud|
|"Are some categories longer than others?"|Box Plot of Word Counts|
|"What are the common phrases?"|N-Gram Bar Chart|

The Universal Data Preprocessing Roadmap
1. Data Cleansing (The Janitor Work)

Handle Missing Values: Decide whether to drop rows with missing data or impute them (filling them with the mean, median, or a logical placeholder).  

Remove Duplicates: Strip out identical rows that could artificially inflate your model's confidence and skew accuracy.

Fix Inconsistencies: Standardize formats across the board to handle noisy data (e.g., ensuring all dates follow the same syntax, or text encodings are uniform).  

2. Data Transformation (The Translation)

Normalize/Scale Numerical Data: Bring vastly different numerical ranges into a uniform scale using Min-Max scaling or Z-score normalization. This ensures large numbers don't overpower smaller, equally important metrics.  

Encode Categorical Data: Machine learning models only read math. Convert text labels (like "High", "Medium", "Low") into numerical matrices using techniques like One-Hot Encoding or Label Encoding


Step 1: Building the Columns (The Features/Vocabulary)

The TF-IDF Vectorizer takes all 622 cleaned requirements.

It scans every single word in all of them.

It picks the top 5000 most useful words and pairs (like "address", "NUM seconds", "user interface").

It writes those 5000 words across the top of a giant whiteboard. These are your Features.

Step 2: Filling the Grid (The X_matrix)

Now, it looks at Requirement #1: "system shall refresh NUM seconds"

It goes down the 5000 columns for Row #1.

If the column says "system", it writes a high math score (like 0.8). If the column says "database", it writes a 0 because that word isn't in the sentence.

It does this 622 times. This giant grid of numbers is your X_matrix.

Step 3: The Answer Key (The y_labels)

This is where you got mixed up! The labels are completely separate from the words.

The y_labels is just a single, straight list of 622 numbers sitting next to the whiteboard.

It simply says:

Row 1's true answer is 0 (Non-Functional).

Row 2's true answer is 1 (Functional).

Row 3's true answer is 0 (Non-Functional).

The Universal Model Building Roadmap
Whenever you reach Step 6 of the Data Science pipeline, you follow these exact five stages, regardless of whether you are predicting stock prices, classifying images, or analyzing text.

1. Data Splitting (The Blindfold Test)

You never let the model see all the data. You split it (usually 80/20).

Training Set (80%): The model looks at the data and the answer key to learn the patterns.

Testing Set (20%): You hide the answer key and force the model to take a "final exam" on data it has never seen before to prove it actually learned the rules, rather than just memorizing the rows.

2. Baseline Establishment

Never start with a massive, complex neural network. You start with the simplest, fastest algorithm possible (like Logistic Regression or Naive Bayes).

This establishes a "floor." If a simple model gets 80% accuracy, you know a complex model must beat 80% to be worth the extra computing power.

3. Model Training & Experimentation

You feed the training data into algorithms (Support Vector Machines, Random Forests, Gradient Boosting) to see which architecture naturally fits the shape of your data.

4. Evaluation (The Report Card)

You run the Testing Set through the trained model and measure performance.

Accuracy: Overall, how many did it get right?

Precision/Recall: Did it accidentally classify too many Functional requirements as Non-Functional (False Positives)?

5. Model Serialization (The Export)

Once you are happy with the accuracy, you freeze the model's "brain" and save it as a file (usually .pkl or .joblib). This allows your web apps or software to use the model instantly without retraining it every time the server boots up.

The Logic for Our Specific Case (PROMISE Dataset)
Because we are doing Text Classification using a massive, sparse TF-IDF matrix (5,000 columns mostly filled with zeros), we need algorithms specifically suited for that architecture.

The Split: We will do an 80/20 split. We will also use a parameter called stratify. This ensures that the 80/20 ratio contains the exact same percentage of Functional and Non-Functional requirements, preventing the model from accidentally training on a batch that is 99% Functional.

The Algorithm: We are using Logistic Regression. Even though it sounds like a math equation, it is an absolute powerhouse for text classification. It draws a highly efficient mathematical boundary through your 5,000-dimensional matrix. We will also use class_weight='balanced' so the model pays extra attention if one category is smaller than the other.

The Evaluation: We will print out the overall Accuracy and a detailed Classification Report to put directly into your final PDF report.  

The Export: We will save requirement_classifier.pkl to power the Streamlit dashboard.