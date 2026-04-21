from fastapi import APIRouter
from urllib.parse import urlparse
import dns.resolver

router = APIRouter()


# 🔥 FIXED DOMAIN CHECK
def domain_exists(url: str) -> bool:
    try:
        # ✅ Ensure scheme (IMPORTANT FIX)
        if not url.startswith("http"):
            url = "http://" + url

        domain = urlparse(url).netloc

        print("🌐 Checking domain:", domain)

        # 🔥 DNS lookup
        dns.resolver.resolve(domain, "A")

        print("✅ Domain exists")
        return True

    except Exception as e:
        print("❌ Domain check failed:", str(e))
        return False


@router.post("/analyze-url")
async def analyze_url(data: dict):

    url = data.get("url", "").lower()
    print("🔥 API HIT with URL:", url)

    # 🚨 STEP 1: DOMAIN VALIDATION
    if not domain_exists(url):
        print("🚨 Invalid domain detected → Suspicious")
        return {
            "fraud_score": 60,
            "risk": "suspicious"
        }

    # 🧠 STEP 2: BASE SCORE
    score = 20

    # 🔴 FRAUD PATTERNS
    if any(x in url for x in [
        "free-money", "win", "bonus", "click-now"
    ]):
        score = 85

    # 🟡 SUSPICIOUS PATTERNS
    elif (
        any(x in url for x in [
            "login", "verify", "account", "secure", "update"
        ]) or
        any(x in url for x in [
            "bit.ly", "tinyurl", "t.co"
        ])
    ):
        score = 45

    # 🎯 FINAL CLASSIFICATION
    if score >= 70:
        risk = "fraud-high"
    elif score >= 40:
        risk = "suspicious"
    else:
        risk = "safe"

    print("📊 FINAL SCORE:", score, "| RISK:", risk)

    return {
        "fraud_score": score,
        "risk": risk
    }