import os
import joblib
import pandas as pd
from urllib.parse import urlparse
import dns.resolver

from app.services.url_feature_extractor import extract_features

# 🔥 PATH SETUP
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../ml-models/url_model/models/url_model.pkl")
)

print("📦 Loading model:", MODEL_PATH)

model = joblib.load(MODEL_PATH)


# 🔥 DOMAIN CHECK
def domain_exists(url: str) -> bool:
    try:
        if not url.startswith("http"):
            url = "http://" + url

        domain = urlparse(url).netloc
        dns.resolver.resolve(domain, "A")
        return True
    except:
        return False


# 🔥 REASON GENERATOR
def generate_reasons(features):

    reasons = []

    if features.get("has_shortener"):
        reasons.append("Uses URL shortener")

    if features.get("phish_hints"):
        reasons.append("Contains phishing keywords")

    if features.get("ip"):
        reasons.append("Uses IP address instead of domain")

    if features.get("length_url", 0) > 80:
        reasons.append("URL is unusually long")

    if features.get("prefix_suffix"):
        reasons.append("Suspicious '-' in domain")

    if not features.get("has_https"):
        reasons.append("Not using HTTPS")

    return reasons


# 🚀 MAIN PREDICTION FUNCTION
def predict_url(url: str):

    url = url.lower()

    # 🚨 STEP 1: DOMAIN CHECK
    if not domain_exists(url):
        return {
            "fraud_score": 60,
            "risk": "suspicious",
            "reasons": ["Domain does not exist"],
            "explanation": "⚠ This domain appears invalid or unreachable."
        }

    # 🚀 STEP 2: FEATURE EXTRACTION
    features = extract_features(url)
    df = pd.DataFrame([features])

    # 🚀 STEP 3: MODEL PREDICTION
    prob = model.predict_proba(df)[0][1]
    score = int(prob * 100)

    # 🔥 THRESHOLD (TUNED)
    if prob >= 0.68:
        risk = "fraud-high"
    elif prob >= 0.40:
        risk = "suspicious"
    else:
        risk = "safe"

    # 🚀 STEP 4: REASONS
    reasons = generate_reasons(features)

    # 🚀 STEP 5: EXPLANATION
    if risk == "fraud-high":
        explanation = "🚨 High risk phishing or scam detected."
    elif risk == "suspicious":
        explanation = "⚠ This looks suspicious. Proceed carefully."
    else:
        explanation = "✅ This appears safe."

    return {
        "fraud_score": score,
        "risk": risk,
        "reasons": reasons,
        "explanation": explanation
    }