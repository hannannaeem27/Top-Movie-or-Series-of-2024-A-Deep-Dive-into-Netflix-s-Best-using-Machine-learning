# -*- coding: utf-8 -*-
"""netflixproject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZaaMwqwzs_qnZ3g080Sj4CTEWNp4Pu6p

**File Reading Code**
"""

import pandas as pd
df = pd.read_csv('/content/ndata.csv', encoding='latin-1')
print("1) 1st 5 rows of the dataset\n2) Last 5 rows of the dataset \n3) Info function \n4) Describe Function.tranform")
fun = input("Enter the function You want to perform: ")
if fun == "1":
  print(df.head())
elif fun == "2":
  print(df.tail())
elif fun == "3":
  print(df.info())
elif fun == "4":
  print(df.describe().T)

"""**SVM Classification Code**"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Convert non-numeric 'Release Year' values (like 'Ongoing') to numeric or median values
df['Release Year'] = pd.to_numeric(df['Release Year'], errors='coerce')
df['Release Year'].fillna(df['Release Year'].median(), inplace=True)

# Drop unnecessary columns
df_cleaned = df.drop(['Title', 'Director', 'Cast'], axis=1)

# Label encode categorical variables
label_encoders = {}
for column in ['Genre', 'Language', 'Type']:
    le = LabelEncoder()
    df_cleaned[column] = le.fit_transform(df_cleaned[column])
    label_encoders[column] = le

# Categorize 'Rating' into High and Low for binary classification
df_cleaned['Rating Category'] = pd.cut(df_cleaned['Rating'], bins=[0, 6, 10], labels=['Low', 'High'])

# Check for class imbalance
print("Class distribution in target variable (Rating Category):")
print(Counter(df_cleaned['Rating Category']))

# Plot the distribution of Ratings
plt.figure(figsize=(8, 5))
sns.histplot(df_cleaned['Rating'], bins=20, kde=True)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.axvline(x=6.5, color='red', linestyle='--', label='Low/High Threshold')
plt.legend()
plt.show()

# Plot a boxplot of ratings by category
plt.figure(figsize=(8, 5))
sns.boxplot(x='Rating Category', y='Rating', data=df_cleaned)
plt.title('Boxplot of Ratings by Category')
plt.xlabel('Rating Category')
plt.ylabel('Rating')
plt.show()

# Split the data into features and target
X = df_cleaned.drop(['Rating', 'Rating Category'], axis=1)
y = df_cleaned['Rating Category']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Initialize the SVM model with class_weight='balanced' to handle class imbalance
svm_model = SVC(kernel='linear', C=1, class_weight='balanced', random_state=42)
svm_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = svm_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Generate the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Generate the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Low', 'High'], yticklabels=['Low', 'High'])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()

# Optional: Visualizing pairwise relationships in the dataset
sns.pairplot(df_cleaned, hue='Rating Category')
plt.title('Pairplot of Features by Rating Category')
plt.show()

"""**Decision Tree Classification code**"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.feature_selection import RFE
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter



# Convert non-numeric 'Release Year' values (e.g., 'Ongoing') to numeric or median values
df['Release Year'] = pd.to_numeric(df['Release Year'], errors='coerce')
df['Release Year'].fillna(df['Release Year'].median(), inplace=True)

# Drop unnecessary columns including 'Language'
df_cleaned = df.drop(['Title', 'Director', 'Cast', 'Language'], axis=1)

# Label encode categorical variables except for 'Language'
label_encoders = {}
for column in ['Genre', 'Type']:
    le = LabelEncoder()
    df_cleaned[column] = le.fit_transform(df_cleaned[column])
    label_encoders[column] = le

# Categorize 'Rating' into High and Low for binary classification
df_cleaned['Rating Category'] = pd.cut(df_cleaned['Rating'], bins=[0, 6.5, 10], labels=['Low', 'High'])

# Check for class imbalance
print("Class distribution in target variable (Rating Category):")
print(Counter(df_cleaned['Rating Category']))

# Plot the distribution of Ratings
plt.figure(figsize=(8, 5))
sns.histplot(df_cleaned['Rating'], bins=20, kde=True)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.axvline(x=6.5, color='red', linestyle='--', label='Low/High Threshold')
plt.legend()
plt.show()

# Plot a boxplot of ratings by category
plt.figure(figsize=(8, 5))
sns.boxplot(x='Rating Category', y='Rating', data=df_cleaned)
plt.title('Boxplot of Ratings by Category')
plt.xlabel('Rating Category')
plt.ylabel('Rating')
plt.show()

# Split the data into features and target
X = df_cleaned.drop(['Rating', 'Rating Category'], axis=1)
y = df_cleaned['Rating Category']

# Standardize the features (optional, but good practice)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Initialize the Decision Tree model with balanced class weights
decision_tree_model = DecisionTreeClassifier(class_weight='balanced', random_state=42)

# Train the Decision Tree model
decision_tree_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = decision_tree_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Generate the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Generate the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Low', 'High'], yticklabels=['Low', 'High'])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()

# Optional: Visualizing pairwise relationships in the dataset
sns.pairplot(df_cleaned, hue='Rating Category')
plt.title('Pairplot of Features by Rating Category')
plt.show()

# Plot feature importance
feature_importance = decision_tree_model.feature_importances_
features = X.columns

# Calculate and print feature importance scores
importance_scores = pd.DataFrame({'Feature': features, 'Importance': feature_importance})
importance_scores = importance_scores.sort_values(by='Importance', ascending=False)

# Print the feature importance scores
print("Feature Importance Scores:")
print(importance_scores)

# Visualize feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_scores)
plt.title('Feature Importance')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()

# Use Recursive Feature Elimination (RFE) to further evaluate feature importance
rfe = RFE(decision_tree_model, n_features_to_select=1)
rfe.fit(X_train, y_train)

# Print the ranking of features based on RFE
ranking = pd.DataFrame({'Feature': features, 'Rank': rfe.ranking_}).sort_values(by='Rank')
print("\nRanking of features using RFE:")
print(ranking)

# Visualize Decision Tree
plt.figure(figsize=(20, 10))
plot_tree(decision_tree_model, feature_names=features, class_names=['Low', 'High'], filled=True)
plt.title('Decision Tree Visualization')
plt.show()

# Function to recommend movies based on genre and optional rating
def recommend_movies(genre, min_rating=None):
    # Filter movies based on the genre
    recommended_movies = df[df['Genre'].str.contains(genre, case=False, na=False)]

    # If a minimum rating is specified, further filter the recommendations
    if min_rating is not None:
        recommended_movies = recommended_movies[recommended_movies['Rating'] >= min_rating]

    if not recommended_movies.empty:
        print(f"\nMovies recommended for the genre '{genre}'")
        if min_rating is not None:
            print(f"with a rating of {min_rating} or higher:\n")
        else:
            print(":\n")

        # Display relevant information about the recommended movies
        print(recommended_movies[['Title', 'Rating', 'Director', 'Release Year', 'Duration (mins)', 'Cast']])
    else:
        print(f"No movies found for the genre '{genre}'" + (f" with a rating of {min_rating} or higher." if min_rating else "."))

# Taking user input for genre and optional rating
user_genre = input("Enter a movie genre: ")
user_rating = input("Enter a minimum rating (or press Enter to skip): ")

# Convert user rating input to float if provided, otherwise set to None
min_rating = float(user_rating) if user_rating else None

# Call the recommendation function
recommend_movies(user_genre, min_rating)

