import math
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any

from app.config import settings


def get_mock_candles(count: int = 180) -> List[Dict[str, Any]]:
    base = 4010.0
    now = datetime.utcnow()
    candles = []

    for i in range(count):
        ts = (now - timedelta(minutes=(count - i))).isoformat()
        drift = (i / count) * 8
        open_price = base + math.sin(i / 8) * 5 + drift
        close_price = open_price + (0.7 if i % 2 == 0 else -0.7) * 3
        high = max(open_price, close_price) + 2.1
        low = min(open_price, close_price) - 2.1
        candles.append({
            "time": ts,
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "close": round(close_price, 2),
            "volume": 100
        })

    return candles


def fetch_oanda_xauusd(timeframe: str = "1M") -> List[Dict[str, Any]]:
    if not settings.OANDA_API_KEY:
        return get_mock_candles()

    granularity_map = {
        "1M": "M1",
        "5M": "M5",
        "15M": "M15",
        "1H": "H1",
        "4H": "H4",
        "1D": "D"
    }

    granularity = granularity_map.get(timeframe, "M1")

    url = f"{settings.OANDA_BASE_URL}/v3/instruments/XAU_USD/candles"
    headers = {
        "Authorization": f"Bearer {settings.OANDA_API_KEY}",
        "Content-Type": "application/json",
    }
    params = {
        "count": 200,
        "granularity": granularity,
        "price": "M"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        if response.status_code != 200:
            return get_mock_candles()

        data = response.json()
        candles = []

        for c in data.get("candles", []):
            candles.append({
                "time": c["time"],
                "open": float(c["mid"]["o"]),
                "high": float(c["mid"]["h"]),
                "low": float(c["mid"]["l"]),
                "close": float(c["mid"]["c"]),
                "volume": 0
            })

        if not candles:
            return get_mock_candles()

        return candles

    except Exception:
        return get_mock_candles()


def get_market_data(timeframe: str = "1M") -> Dict[str, Any]:
    candles = fetch_oanda_xauusd(timeframe)
    df = pd.DataFrame(candles)
    if df.empty:
        return {"symbol": "XAUUSD", "price": 0.0, "change_percent": 0.0, "timeframe": timeframe, "candles": []}

    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").reset_index(drop=True)

    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    price = float(last["close"])
    prev_price = float(prev["close"])
    change_percent = ((price - prev_price) / prev_price) * 100 if prev_price else 0.0

    return {
        "symbol": "XAUUSD",
        "price": round(price, 2),
        "change_percent": round(change_percent, 2),
        "timeframe": timeframe,
        "candles": df.to_dict(orient="records"),
    }
