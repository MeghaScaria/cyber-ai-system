import pickle
import os

# 🔥 Load model paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "../../../ml-models/saved_models/text_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "../../../ml-models/saved_models/vectorizer.pkl")

# 🔥 Load model once (on startup)
model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


async def analyze_text(message: str):
    text = message.lower()

    # 🔹 Convert text → vector
    text_vec = vectorizer.transform([message])

    # 🔹 ML Prediction
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0][1]

    is_fraud_ml = bool(prediction)
    score = int(probability * 100)

    reasons = []

    # 🔥 ML reasoning
    if is_fraud_ml:
        reasons.append("ML model detected fraud pattern")

    # 🔥 Rule-based boosts (VERY IMPORTANT)
    if "otp" in text:
        score += 20
        reasons.append("OTP keyword detected")

    if "bank" in text:
        score += 10
        reasons.append("Bank-related message")

    if "urgent" in text or "now" in text:
        score += 10
        reasons.append("Urgency detected")

    if "click" in text or "link" in text:
        score += 10
        reasons.append("Suspicious link instruction")

    # 🔹 Cap score
    score = min(score, 100)

    # 🔹 Final decision (hybrid)
    is_fraud = score >= 50

    # 🔹 If nothing detected
    if not reasons:
        reasons.append("No suspicious patterns detected")

    return {
        "is_fraud": is_fraud,
        "score": score,
        "reasons": reasons
    }