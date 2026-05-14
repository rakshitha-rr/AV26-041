"""
🌾 Smart Agriculture Intelligence System
Main FastAPI Application — Entry Point

Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models.yield_model import load_model, get_model_metrics
from routes import prediction, simulation, risk_alerts, heatmap, soil, disease, schemes, communication, offline, auth, history, voice
from db.redis_client import connect_redis, close_redis
from db.mongo import connect_mongo, close_mongo
import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize ML model and Databases on startup."""
    print("\n" + "=" * 60)
    print(" Smart Agriculture Intelligence System")
    print("=" * 60)
    
    # Init ML
    load_model()
    metrics = get_model_metrics()
    if metrics:
        print(f" Model R2 Score: {metrics.get('r2_score', 'N/A')}")
        print(f" Model MAE: {metrics.get('mae', 'N/A')}")
        
    # Init DBs
    await connect_redis()
    await connect_mongo()
    
    # Ensure temp audio dir exists
    os.makedirs(os.path.join(os.path.dirname(__file__), "temp_audio"), exist_ok=True)
    
    print(" System ready!")
    print("=" * 60 + "\n")
    yield
    print("\n Shutting down...")
    await close_redis()
    await close_mongo()


app = FastAPI(
    title=" Smart Agriculture Intelligence System",
    description=(
        "ML-powered Crop Yield Prediction Engine with What-If Simulator, "
        "Risk Alerts, Zone Heatmaps, Soil Analysis, Disease Detection, "
        "Government Schemes, and SMS/WhatsApp Integration.\n\n"
        "**Core Module:** Crop Yield Prediction using RandomForest ML Model\n"
        "**Target Region:** Karnataka, India"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routes ────────────────────────────────────────────
app.include_router(auth.router, prefix="/api")
app.include_router(voice.router, prefix="/api/voice")
app.include_router(sms.router, prefix="/api")
app.include_router(prediction.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")
app.include_router(risk_alerts.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(heatmap.router, prefix="/api")
app.include_router(soil.router, prefix="/api")
app.include_router(disease.router, prefix="/api")
app.include_router(schemes.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Welcome to the AgriIntel Smart Agriculture Intelligence System",
        "region": "Karnataka, India",
        "core_module": "Crop Yield Prediction Engine (RandomForest ML)",
        "endpoints": {
            "login": "POST /api/login",
            "logout": "POST /api/logout",
            "predict_yield": "POST /api/predict-yield",
            "simulate_yield": "POST /api/simulate-yield",
            "risk_alerts": "POST /api/risk-alerts",
            "prediction_history": "GET /api/history",
            "alerts_history": "GET /api/alerts/history",
            "voice_assistant": "POST /api/voice/voice-assistant",
            "send_sms": "POST /api/send-sms",
            "sms_webhook": "POST /api/webhook/sms",
            "voice_webhook": "POST /api/webhook/voice",
            "offline_query": "POST /api/offline-query",
            "yield_heatmap": "GET /api/yield-heatmap",
            "soil_analysis": "POST /api/soil-analysis",
            "government_schemes": "GET /api/schemes",
        },
        "docs": "/docs",
    }


@app.get("/health", tags=["🏠 Home"])
async def health_check():
    metrics = get_model_metrics()
    return {
        "status": "healthy",
        "model_loaded": metrics is not None and len(metrics) > 0,
        "model_metrics": metrics,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
