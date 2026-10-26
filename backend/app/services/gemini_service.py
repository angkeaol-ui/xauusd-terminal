import requests
from app.config import settings


def summarize_market_with_gemini(signal_data: dict, price: float, timeframe: str) -> str:
    if not settings.GEMINI_API_KEY:
        return signal_data.get("ai_summary", "Market summary unavailable")

    prompt = f"""
    You are a market analyst reviewing XAUUSD.
    Use these values:
    - timeframe: {timeframe}
    - spot price: {price}
    - signal: {signal_data.get('signal')}
    - confidence: {signal_data.get('confidence')}
    - trend: {signal_data.get('trend')}
    - RSI: {signal_data.get('rsi')}
    - MACD: {signal_data.get('macd')}
    - ATR: {signal_data.get('atr')}
    - support: {signal_data.get('support')}
    - resistance: {signal_data.get('resistance')}
    - entry: {signal_data.get('entry')}
    - stop loss: {signal_data.get('stop_loss')}
    - take profit 1: {signal_data.get('take_profit_1')}
    - take profit 2: {signal_data.get('take_profit_2')}

    Provide a concise but professional market analysis in plain English.
    Keep it factual, not promotional.
    Do not claim guaranteed profits.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()

        candidates = result.get("candidates", [])
        if not candidates:
            return signal_data.get("ai_summary", "Market summary unavailable")

        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if text:
            return text.strip()

        return signal_data.get("ai_summary", "Market summary unavailable")
    except Exception:
        return signal_data.get("ai_summary", "Market summary unavailable")
