import os
import sys
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

# 🔥 PATH FIX
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../../backend"))

sys.path.append(BACKEND_PATH)

from app.services.url_feature_extractor import extract_features

# 🔥 FILE PATHS
DATA_PATH = os.path.join(BASE_DIR, "../../data/processed/phishing_urls_selected_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../models/url_model.pkl")

print("📂 Loading data from:", DATA_PATH)

# 🔥 LOAD DATA
df = pd.read_csv(DATA_PATH)

# 🔥 CLEAN DATA
df = df.drop_duplicates()

if "url" not in df.columns or "label" not in df.columns:
    raise ValueError("❌ Dataset must contain 'url' and 'label' columns")

print("✅ Dataset size:", len(df))

# 🚀 FEATURE EXTRACTION (VERY IMPORTANT)
print("🔧 Extracting features...")

X = df["url"].apply(extract_features).apply(pd.Series)
y = df["label"]

print("✅ Features shape:", X.shape)

# 🔥 SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 🚀 MODEL (TUNED)
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=1.2,   # 🔥 CHANGE HERE
    eval_metric="logloss",
    random_state=42
)

# 🔥 TRAIN
print("🚀 Training model...")
model.fit(X_train, y_train)

# 🔍 CROSS VALIDATION
print("\n🔍 Running Cross-Validation...")
scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc")
print("CV ROC-AUC:", scores.mean())

# 📊 EVALUATION
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

print("\n=== REPORT ===")
print(classification_report(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))

# 💾 SAVE MODEL
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ MODEL TRAINED & SAVED at:", MODEL_PATH)