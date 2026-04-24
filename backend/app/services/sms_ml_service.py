import os
import joblib

# 🔥 BASE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ CORRECT PATHS (FIXED)
MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../ml-models/text_model/saved_models/text_model.pkl")
)

VECTORIZER_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../ml-models/text_model/saved_models/vectorizer.pkl")
)

# 🔍 DEBUG PATH (VERY USEFUL)
print("📦 Loading SMS model from:", MODEL_PATH)
print("📦 Loading vectorizer from:", VECTORIZER_PATH)

# 🚨 SAFE LOAD (PREVENT CRASH)
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ SMS model not found at: {MODEL_PATH}")

if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(f"❌ Vectorizer not found at: {VECTORIZER_PATH}")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# 🚀 REASON GENERATOR
def generate_sms_reasons(text: str):
    text_lower = text.lower()
    reasons = []

    if any(word in text_lower for word in ["win", "won", "prize", "reward", "gift"]):
        reasons.append("Contains prize/offer keywords")

    if any(word in text_lower for word in ["urgent", "immediately", "now", "hurry"]):
        reasons.append("Creates urgency pressure")

    if any(word in text_lower for word in ["click", "link", "http", "bit.ly"]):
        reasons.append("Contains suspicious link")

    if any(word in text_lower for word in ["bank", "account", "verify", "otp"]):
        reasons.append("Requests sensitive information")

    if any(char.isdigit() for char in text_lower):
        reasons.append("Contains numeric bait (money/amount)")

    return reasons


# 🚀 MAIN PREDICT FUNCTION
def predict_sms(text: str):

    if not text or not text.strip():
        return {
            "fraud_score": 0,
            "risk": "safe",
            "reasons": [],
            "explanation": "No message provided."
        }

    # 🔥 VECTORIZE
    vec = vectorizer.transform([text])

    # 🔥 MODEL PREDICTION
    prob = model.predict_proba(vec)[0][1]
    score = int(prob * 100)

    # 🎯 THRESHOLD (PRO TUNED)
    if prob >= 0.75:
        risk = "fraud-high"
    elif prob >= 0.45:
        risk = "suspicious"
    else:
        risk = "safe"

    # 🔥 REASONS
    reasons = generate_sms_reasons(text)

    # 🔥 EXPLANATION
    if risk == "fraud-high":
        explanation = "🚨 This SMS is highly likely to be a scam."
    elif risk == "suspicious":
        explanation = "⚠ This SMS looks suspicious. Be careful."
    else:
        explanation = "✅ This SMS appears safe."

    return {
        "fraud_score": score,
        "risk": risk,
        "reasons": reasons,
        "explanation": explanation
    }