from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse
import dns.resolver

from app.services.url_ml_service import predict_url
from app.api.routes.sms_routes import router as sms_router

app = FastAPI(title="Fraud AI Shield API")


# ==========================
# 🔹 REQUEST MODEL
# ==========================
class URLRequest(BaseModel):
    url: str


# ==========================
# 🔐 TRUSTED DOMAINS
# ==========================
TRUSTED_DOMAINS = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "amazon.in",
    "microsoft.com",
    "openai.com"
]


def is_trusted(url: str) -> bool:
    domain = urlparse(url).netloc.replace("www.", "")
    return any(td in domain for td in TRUSTED_DOMAINS)


# ==========================
# 🌐 DOMAIN CHECK
# ==========================
def domain_exists(url: str) -> bool:
    try:
        if not url.startswith("http"):
            url = "http://" + url

        domain = urlparse(url).netloc
        dns.resolver.resolve(domain, "A")
        return True
    except:
        return False


# ==========================
# 🚀 URL ANALYSIS (FINAL)
# ==========================
@app.post("/analyze-url", tags=["URL"])
async def analyze_url(data: URLRequest):

    url = data.url.lower()
    print("🔥 URL RECEIVED:", url)

    # ✅ 1. TRUSTED DOMAIN
    if is_trusted(url):
        return {
            "fraud_score": 5,
            "risk": "safe",
            "reasons": ["Trusted domain"],
            "explanation": "✅ This is a well-known trusted website.",
            "status": "trusted"
        }

    # 🚨 2. INVALID DOMAIN (FIXED LOGIC)
    if not domain_exists(url):
        return {
            "fraud_score": 20,
            "risk": "suspicious",
            "reasons": ["Domain unreachable or invalid"],
            "explanation": "⚠ This domain could not be verified. It may be unsafe.",
            "status": "invalid"
        }

    # 🤖 3. ML + HYBRID SCORING
    result = predict_url(url)

    # 🔥 Ensure status exists
    result["status"] = "valid"

    return result


# ==========================
# 🚀 REGISTER SMS ROUTES
# ==========================
app.include_router(sms_router)