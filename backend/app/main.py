from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import (
    connect_to_mongo,
    close_mongo_connection
)

from app.database.mongo import save_analysis_result

from app.api.routes.history import router as history_router
from app.api.routes.fraud_routes import router as fraud_router

from app.services.text_detection import analyze_text


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_to_mongo()

    yield

    await close_mongo_connection()


app = FastAPI(
    title="Fraud AI Shield API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# REQUEST MODELS
# ==========================
class SMSRequest(BaseModel):
    message: str


# ==========================
# SMS ANALYSIS
# ==========================
@app.post("/analyze-sms", tags=["SMS"])
async def analyze_sms(data: SMSRequest):

    result = await analyze_text(data.message)

    response = {
        "fraud_score": result["score"],
        "risk": "fraud-high" if result["is_fraud"] else "safe",
        "reasons": result["reasons"]
    }

    # SAVE TO DATABASE
    await save_analysis_result(
        user_id="guest_user",
        result={
            "type": "sms",
            "content": data.message,
            **response
        }
    )
    
    await manager.broadcast({
        "type": "fraud_update",
        "data": result
    })
    return response


# ==========================
# REGISTER ROUTES
# ==========================
app.include_router(history_router)
app.include_router(fraud_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)