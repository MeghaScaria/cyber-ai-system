import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("data/raw/spam_ham_india_combined_dataset.csv")

# ✅ Handle missing values
df = df.dropna(subset=["Message", "Category"])

print(df.head())

# ✅ Correct columns
X = df["Message"]
y = df["Category"]

# ✅ Convert labels
y = y.map({"ham": 0, "spam": 1})

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Vectorize
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Train model
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Save
os.makedirs("saved_models", exist_ok=True)

pickle.dump(model, open("saved_models/text_model.pkl", "wb"))
pickle.dump(vectorizer, open("saved_models/vectorizer.pkl", "wb"))

print("✅ Model trained and saved!")