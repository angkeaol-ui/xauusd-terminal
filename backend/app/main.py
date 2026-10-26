from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from app.services.market_service import get_market_data
from app.services.signal_engine import generate_signal
from app.services.gemini_service import summarize_market_with_gemini

app = FastAPI(title="XAUUSD Terminal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/market/xauusd")
def get_market(timeframe: str = Query("1M", alias="timeframe")):
    return get_market_data(timeframe)

@app.post("/api/analyze")
def analyze(timeframe: str = "1M"):
    data = get_market_data(timeframe)
    candles = data.get("candles", [])
    df = pd.DataFrame(candles)

    if df.empty:
        return {
            "signal": "HOLD",
            "confidence": 0.0,
            "entry": 0.0,
            "stop_loss": 0.0,
            "take_profit_1": 0.0,
            "take_profit_2": 0.0,
            "risk_reward": 0.0,
            "trend": "neutral",
            "rsi": 50.0,
            "macd": 0.0,
            "atr": 0.0,
            "support": 0.0,
            "resistance": 0.0,
            "ai_summary": "No market data available"
        }

    signal = generate_signal(df)
    ai_summary = summarize_market_with_gemini(signal, data.get("price", 0), timeframe)
    signal["ai_summary"] = ai_summary
    return signal

@app.post("/api/ai-summary")
def ai_summary(timeframe: str = "1M"):
    data = get_market_data(timeframe)
    candles = data.get("candles", [])
    df = pd.DataFrame(candles)
    signal = generate_signal(df)
    return {
        "summary": summarize_market_with_gemini(signal, data.get("price", 0), timeframe)
    }
