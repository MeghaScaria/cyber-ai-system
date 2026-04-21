from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse
import dns.resolver

app = FastAPI()


# 🔹 Request Model
class URLRequest(BaseModel):
    url: str


# 🔥 DOMAIN CHECK (FIXED)
def domain_exists(url: str) -> bool:
    try:
        if not url.startswith("http"):
            url = "http://" + url

        domain = urlparse(url).netloc

        print("🌐 Checking domain:", domain)

        dns.resolver.resolve(domain, "A")

        print("✅ Domain exists")
        return True

    except Exception as e:
        print("❌ Domain not found:", e)
        return False


# 🔥 MAIN API
@app.post("/analyze-url", tags=["Extension"])
async def analyze_url(data: URLRequest):

    url = data.url.lower()
    print("🔥 URL RECEIVED:", url)

    # 🚨 STEP 1: DOMAIN VALIDATION
    if not domain_exists(url):
        return {
            "fraud_score": 60,
            "risk": "suspicious"
        }

    # 🧠 STEP 2: BASE SCORE
    score = 20

    # 🔴 STRONG FRAUD (ONLY HIGH SIGNALS)
    if any(x in url for x in [
        "free-money", "win", "bonus", "click-now"
    ]):
        score = 85

    # 🟡 SUSPICIOUS (YELLOW ZONE)
    elif any(x in url for x in [
        "login", "verify", "bank", "secure", "update"
    ]):
        score = 45

    # 🟡 SHORT LINKS
    elif any(x in url for x in [
        "bit.ly", "tinyurl", "t.co"
    ]):
        score = 45

    # 🎯 FINAL CLASSIFICATION
    if score >= 70:
        risk = "fraud-high"
    elif score >= 40:
        risk = "suspicious"
    else:
        risk = "safe"

    print("📊 FINAL:", score, risk)

    return {
        "fraud_score": score,
        "risk": risk
    }