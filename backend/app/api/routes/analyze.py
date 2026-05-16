<<<<<<< HEAD
from fastapi import APIRouter, Depends
from app.schemas.request_schema import MessageAnalysisRequest
from app.schemas.response_schema import AnalysisResponse
from app.services import text_detection, url_detection, anomaly_detection

router = APIRouter()

@router.post("/analyze-message", response_model=AnalysisResponse)
async def analyze_message(request: MessageAnalysisRequest):
    """
    Analyzes a message for fraud, phishing URLs, and anomalies.
    """
    # Placeholder logic
    text_result = await text_detection.analyze_text(request.message)
    url_result = await url_detection.check_urls(request.message)
    anomaly_result = await anomaly_detection.check_anomaly(request.user_id, request.metadata)
    
    return {
        "is_fraud": text_result["is_fraud"],
        "fraud_score": text_result["score"],
        "phishing_detected": url_result["detected"],
        "anomaly_detected": anomaly_result["anomaly"],
        "risk_level": "low" # placeholder aggregated risk
    }
=======
from fastapi import APIRouter
from urllib.parse import urlparse
import dns.resolver
import joblib
import pandas as pd
import re
import os

router = APIRouter()

# =========================
# 🔥 LOAD MODEL
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../../ml-models/url_model/models/url_model.pkl")
)

print("📦 Loading model from:", MODEL_PATH)
model = joblib.load(MODEL_PATH)

# =========================
# 🔐 TRUSTED DOMAINS
# =========================
TRUSTED_DOMAINS = [
    "google.com", "youtube.com", "facebook.com",
    "amazon.in", "microsoft.com", "openai.com"
]

def is_trusted(url: str) -> bool:
    try:
        domain = urlparse(url).netloc.lower().replace("www.", "")
        return any(domain == t or domain.endswith("." + t) for t in TRUSTED_DOMAINS)
    except:
        return False

# =========================
# 🚀 FEATURE EXTRACTOR
# =========================
def extract_features(url: str):

    if not url.startswith("http"):
        url = "http://" + url

    p = urlparse(url)
    domain = p.netloc
    path = p.path

    words_host = [w for w in domain.split(".") if w]
    words_path = [w for w in path.split("/") if w]

    return {
        "ratio_digits_url": sum(c.isdigit() for c in url) / max(len(url), 1),
        "ip": int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", domain))),
        "nb_qm": url.count("?"),
        "length_url": len(url),
        "nb_slash": url.count("/"),
        "length_hostname": len(domain),
        "nb_eq": url.count("="),
        "ratio_digits_host": sum(c.isdigit() for c in domain) / max(len(domain), 1),
        "shortest_word_host": min([len(w) for w in words_host] or [0]),
        "prefix_suffix": int("-" in domain),
        "longest_word_path": max([len(w) for w in words_path] or [0]),
        "tld_in_subdomain": int(len(words_host) > 2),

        # 🔥 EXTRA SIGNALS
        "phish_hints": int(any(w in url for w in [
            "login", "verify", "secure", "update", "account",
            "free", "win", "bonus", "claim", "reward"
        ])),
        "has_https": int(url.startswith("https")),
        "num_dots": url.count("."),
        "has_shortener": int(any(x in url for x in ["bit.ly", "tinyurl", "t.co"]))
    }

# =========================
# 🌐 DOMAIN CHECK
# =========================
def domain_exists(url: str) -> bool:
    try:
        if not url.startswith("http"):
            url = "http://" + url
        domain = urlparse(url).netloc
        dns.resolver.resolve(domain, "A")
        return True
    except:
        return False

# =========================
# 🧠 HYBRID SCORING ENGINE
# =========================
def compute_rule_score(features):

    score = 0

    if features["phish_hints"]:
        score += 25

    if features["has_shortener"]:
        score += 20

    if features["ip"]:
        score += 30

    if features["length_url"] > 80:
        score += 10

    if features["prefix_suffix"]:
        score += 10

    if not features["has_https"]:
        score += 10

    return min(score, 100)  # cap at 100

# =========================
# 🧠 REASONS
# =========================
def generate_reasons(features):

    reasons = []

    if features["has_shortener"]:
        reasons.append("Uses URL shortener")

    if features["phish_hints"]:
        reasons.append("Contains phishing keywords")

    if features["ip"]:
        reasons.append("Uses IP address instead of domain")

    if features["length_url"] > 80:
        reasons.append("URL is unusually long")

    if features["prefix_suffix"]:
        reasons.append("Suspicious '-' in domain")

    if not features["has_https"]:
        reasons.append("Not using HTTPS")

    return reasons

# =========================
# 🚀 MAIN API
# =========================
@router.post("/analyze-url")
async def analyze_url(data: dict):

    url = data.get("url", "").lower()
    print("🔥 API HIT:", url)

    # 🔐 TRUSTED OVERRIDE
    if is_trusted(url):
        return {
            "fraud_score": 5,
            "risk": "safe",
            "reasons": ["Trusted domain"],
            "explanation": "✅ This is a well-known trusted website."
        }

    # 🚨 DOMAIN CHECK
    if not domain_exists(url):
        return {
            "fraud_score": 60,
            "risk": "suspicious",
            "reasons": ["Domain does not exist"],
            "explanation": "⚠ This domain appears invalid or unsafe."
        }

    # 🔍 FEATURES
    features = extract_features(url)
    df = pd.DataFrame([features])

    # 🤖 ML SCORE
    ml_prob = model.predict_proba(df)[0][1]   # 0–1
    ml_score = ml_prob * 100

    # 🧠 RULE SCORE
    rule_score = compute_rule_score(features)

    # 🔥 HYBRID COMBINATION
    final_score = int((ml_score * 0.7) + (rule_score * 0.3))

    # 🎯 CLASSIFICATION
    if final_score >= 70:
        risk = "fraud-high"
    elif final_score >= 40:
        risk = "suspicious"
    else:
        risk = "safe"

    # 🧠 REASONS
    reasons = generate_reasons(features)

    # 💬 EXPLANATION
    if risk == "fraud-high":
        explanation = "🚨 High risk phishing detected based on multiple risk signals."
    elif risk == "suspicious":
        explanation = "⚠ This URL shows suspicious patterns. Proceed carefully."
    else:
        explanation = "✅ This appears safe based on current analysis."

    print(f"📊 ML: {ml_score:.2f} | Rule: {rule_score} | Final: {final_score}")

    return {
        "fraud_score": final_score,
        "risk": risk,
        "reasons": reasons,
        "explanation": explanation
    }
>>>>>>> a0f7da8cc7fad890039a870d1c17f00d427434cc
