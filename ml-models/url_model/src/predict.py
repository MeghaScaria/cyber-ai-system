import joblib
import pandas as pd
from features import extract_features

MODEL_PATH = "../models/url_model.pkl"
model = joblib.load(MODEL_PATH)

def predict_url(url: str):
    feats = extract_features(url)
    df = pd.DataFrame([feats])
    prob = model.predict_proba(df)[0][1]
    score = int(prob * 100)

    if score >= 70:
        risk = "fraud-high"
    elif score >= 40:
        risk = "suspicious"
    else:
        risk = "safe"

    return score, risk

if __name__ == "__main__":
    tests = [
        "https://google.com",
        "http://bit.ly/verify-account",
        "http://free-money-click-now.com"
    ]
    for t in tests:
        print(t, "→", predict_url(t))