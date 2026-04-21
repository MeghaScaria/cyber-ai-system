<<<<<<< Updated upstream
import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analyze, history, risk, auth
from app.config.settings import settings
=======
from fastapi import FastAPI
from app.api.routes import auth, analyze, history, risk, token_routes, fraud_routes
from app.config.database import connect_to_mongo, close_mongo_connection
from app.config.settings import settings
import logging
>>>>>>> Stashed changes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
<<<<<<< Updated upstream
    title="Cyber AI System API",
    description="Backend API for AI-powered cyber safety and fraud detection",
    version="1.0.0"
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred. Please try again later."},
    )

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"path={request.url.path} method={request.method} duration={process_time:.4f}s status={response.status_code}")
    return response

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, tags=["Analyze"])
app.include_router(history.router, tags=["History"])
app.include_router(risk.router, tags=["Risk"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
=======
    title=settings.APP_NAME,
    description="Backend API for Cyber AI System - AI-driven fraud and phishing detection.",
    version="1.0.0"
)

# 🔄 Database Lifecycle
@app.on_event("startup")
async def startup_db_client():
    try:
        await connect_to_mongo()
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    logger.info("Successfully closed MongoDB connection")

# 🛣️ Include Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["Analysis"])
app.include_router(analyze.router, tags=["Legacy Support"]) # Compatibility for Chrome Extension
app.include_router(history.router, prefix="/api/v1/history", tags=["User History"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["Risk Management"])
app.include_router(token_routes.router, prefix="/api/v1/tokens", tags=["Token Management"])
app.include_router(fraud_routes.router, prefix="/api/v1/fraud", tags=["Fraud Analysis"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "status": "online"
    }
>>>>>>> Stashed changes
