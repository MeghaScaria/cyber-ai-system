import pickle
import os
import logging

logger = logging.getLogger(__name__)

# 🔥 Load model paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: In production, these should be configurable via Settings
model_path = os.path.join(BASE_DIR, "../../../ml-models/saved_models/text_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "../../../ml-models/saved_models/vectorizer.pkl")

# 🔥 Load model with fallback
model = None
vectorizer = None

def load_ml_models():
    global model, vectorizer
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            with open(vectorizer_path, "rb") as f:
                vectorizer = pickle.load(f)
            logger.info("✅ ML models loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"❌ Error loading ML models: {e}")
            return False
    else:
        logger.warning("🧠 ML models not found. Falling back to rule-based analysis only.")
        return False

# Attempt load on import
load_ml_models()

async def analyze_text(message: str):
    text = message.lower()
    reasons = []
    score = 0
    
    # 🔹 ML Prediction (if available)
    if model and vectorizer:
        try:
            text_vec = vectorizer.transform([message])
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0][1]
            if bool(prediction):
                reasons.append("ML model detected fraud pattern")
            score = int(probability * 100)
        except Exception as e:
            logger.error(f"❌ ML inference error: {e}")
            score = 20 # Base suspicious score on failure
    else:
        # Initial base score when ML is missing
        score = 20

    # 🔥 Rule-based boosts (EXTREMELY IMPORTANT when ML is missing)
    if "otp" in text:
        score += 25
        reasons.append("OTP keyword detected")

    if any(x in text for x in ["bank", "sbi", "hdfc", "icici"]):
        score += 15
        reasons.append("Bank-related keywords")

    if any(x in text for x in ["urgent", "now", "immediately", "expired"]):
        score += 15
        reasons.append("Sense of urgency")

    if any(x in text for x in ["click", "link", "http", "www"]):
        score += 15
        reasons.append("Request to click link")
        
    if "gift" in text or "win" in text or "prize" in text:
        score += 20
        reasons.append("Rewards/Lottery offer detected")

    # 🔹 Cap score
    score = min(score, 100)

    # 🔹 Final decision (hybrid)
    is_fraud = score >= 50

    # 🔹 If nothing detected
    if not reasons:
        reasons.append("No common suspicious patterns detected")

    return {
        "is_fraud": is_fraud,
        "score": score,
        "reasons": reasons
    }
