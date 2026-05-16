from fastapi import APIRouter
from urllib.parse import urlparse
import dns.resolver
import joblib
import pandas as pd
import re
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../../ml-models/url_model/models/url_model.pkl")
)

print("📦 Loading model from:", MODEL_PATH)
model = joblib.load(MODEL_PATH)


# ✅ TRUSTED DOMAINS
TRUSTED_DOMAINS = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "amazon.in",
    "microsoft.com",
    "openai.com"
]


def is_trusted(url):
    domain = urlparse(url).netloc.replace("www.", "")
    return any(td in domain for td in TRUSTED_DOMAINS)


# 🚀 FEATURE EXTRACTOR
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
        "phish_hints": int(any(w in url for w in [
            "login", "verify", "secure", "update", "account",
            "free", "win", "bonus", "claim", "reward"
        ])),
        "has_https": int(url.startswith("https")),
        "num_dots": url.count("."),
        "has_shortener": int(any(x in url for x in ["bit.ly", "tinyurl", "t.co"]))
    }


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


# 🚀 REASONS
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


# 🚀 MAIN API
@router.post("/analyze-url")
async def analyze_url(data: dict):

    url = data.get("url", "").lower()
    print("🔥 API HIT:", url)

    # ✅ TRUSTED FIRST
    if is_trusted(url):
        return {
            "fraud_score": 5,
            "risk": "safe",
            "reasons": ["Trusted domain"],
            "explanation": "✅ This is a well-known trusted website."
        }

    # 🚨 INVALID DOMAIN (FIXED)
    if not domain_exists(url):
        return {
            "fraud_score": 20,   # 👈 reduced
            "risk": "suspicious",
            "reasons": ["Domain unreachable or invalid"],
            "explanation": "⚠ This domain could not be verified. It may be unsafe.",
            "status": "invalid"   # 👈 NEW FLAG
        }

    # 🚀 NORMAL FLOW
    features = extract_features(url)
    df = pd.DataFrame([features])

    prob = model.predict_proba(df)[0][1]

    # 🔥 HYBRID BOOST
    boost = 0
    if features["has_shortener"]:
        boost += 0.15
    if features["phish_hints"]:
        boost += 0.20
    if not features["has_https"]:
        boost += 0.10

    final_prob = min(prob + boost, 1.0)

    score = int(final_prob * 100)

    # 🚀 CLASSIFICATION
    if final_prob >= 0.75:
        risk = "fraud-high"
    elif final_prob >= 0.40:
        risk = "suspicious"
    else:
        risk = "safe"

    reasons = generate_reasons(features)

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
        "explanation": explanation,
        "status": "valid"
    }