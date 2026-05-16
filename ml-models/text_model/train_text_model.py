import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 📂 PATH SETUP
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../data/raw/spam_ham_india_combined_dataset.csv")
)

MODEL_PATH = os.path.join(BASE_DIR, "saved_models/text_model.pkl")
VEC_PATH = os.path.join(BASE_DIR, "saved_models/vectorizer.pkl")

print("📂 Loading dataset from:", DATA_PATH)

# 🔥 LOAD DATA
df = pd.read_csv(DATA_PATH)

print("📊 Columns:", df.columns)

# 🔥 AUTO DETECT COLUMNS (VERY IMPORTANT)
# Try to find text + label automatically
text_col = None
label_col = None

for col in df.columns:
    if "text" in col.lower() or "message" in col.lower() or "sms" in col.lower():
        text_col = col
    if "label" in col.lower() or "type" in col.lower() or "category" in col.lower():
        label_col = col

if text_col is None or label_col is None:
    raise ValueError("❌ Could not detect text/label columns. Print df.head() and fix manually.")

# 🔥 RENAME
df = df[[label_col, text_col]]
df.columns = ["label", "text"]

# 🔥 CLEAN LABELS
df["label"] = df["label"].astype(str).str.lower()

df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1,
    "0": 0,
    "1": 1
})

# Remove nulls
df = df.dropna()

print("✅ Dataset size:", len(df))

# 🚀 SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# 🔥 TF-IDF
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 🔥 MODEL
model = LogisticRegression(max_iter=1000, class_weight="balanced")

print("🚀 Training SMS model...")
model.fit(X_train_vec, y_train)

# 📊 EVALUATION
pred = model.predict(X_test_vec)

print("\n=== SMS MODEL REPORT ===")
print(classification_report(y_test, pred))

# 💾 SAVE
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VEC_PATH)

print("✅ SMS MODEL SAVED")