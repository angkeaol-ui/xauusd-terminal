from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

from app.services.market_service import get_market_data
from app.services.signal_engine import generate_signal
from app.services.gemini_service import chat_with_gemini, summarize_market_with_gemini

app = FastAPI(title="XAUUSD Terminal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    signal: dict | None = None
    price: float | None = None
    timeframe: str = "1M"


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


@app.post("/api/ai/chat")
def ai_chat(payload: ChatRequest):
    context = ""

    if payload.signal:
        context += f"Signal: {payload.signal.get('signal')}\n"
        context += f"Confidence: {payload.signal.get('confidence')}\n"
        context += f"Trend: {payload.signal.get('trend')}\n"
        context += f"RSI: {payload.signal.get('rsi')}\n"
        context += f"MACD: {payload.signal.get('macd')}\n"
        context += f"ATR: {payload.signal.get('atr')}\n"
        context += f"Entry: {payload.signal.get('entry')}\n"
        context += f"Stop Loss: {payload.signal.get('stop_loss')}\n"
        context += f"Take Profit: {payload.signal.get('take_profit_1')}\n"

    if payload.price is not None:
        context += f"Current price: {payload.price}\n"

    prompt = f"""
    You are a professional XAUUSD market analyst.
    Context:
    {context}

    User question:
    {payload.question}

    Answer in clear English. Keep it practical and factual.
    Do not promise profits.
    """

    return {"answer": chat_with_gemini(prompt)}
