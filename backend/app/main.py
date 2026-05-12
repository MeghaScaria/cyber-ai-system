from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse
import dns.resolver

from app.api.routes.history import router as history_router

from app.database.mongo import save_analysis_result

from app.services.url_ml_service import predict_url
from app.api.routes.sms_routes import router as sms_router


from contextlib import asynccontextmanager
from app.config.database import connect_to_mongo, close_mongo_connection

#######
from app.config.settings import settings



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Fraud AI Shield API",
    lifespan=lifespan
)
#########

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

    # ✅ TRUSTED DOMAIN
    if is_trusted(url):

        result = {
            "fraud_score": 5,
            "risk": "safe",
            "reasons": ["Trusted domain"],
            "explanation": "✅ This is a well-known trusted website.",
            "status": "trusted"
        }

    # 🚨 INVALID DOMAIN
    elif not domain_exists(url):

        result = {
            "fraud_score": 20,
            "risk": "suspicious",
            "reasons": ["Domain unreachable or invalid"],
            "explanation": "⚠ This domain could not be verified. It may be unsafe.",
            "status": "invalid"
        }

    # 🤖 ML ANALYSIS
    else:

        result = predict_url(url)

        result["status"] = "valid"

    # 💾 SAVE TO MONGODB
    await save_analysis_result(
        user_id="guest_user",
        result={
            "type": "url",
            "content": url,
            **result
        }
    )

    return result


# ==========================
# 🚀 REGISTER SMS ROUTES
# ==========================
app.include_router(sms_router)
app.include_router(history_router)