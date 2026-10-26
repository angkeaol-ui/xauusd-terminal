from pydantic import BaseModel
from typing import List

class Candle(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: int = 0

class MarketResponse(BaseModel):
    symbol: str
    price: float
    change_percent: float
    timeframe: str
    candles: List[Candle]

class SignalResponse(BaseModel):
    symbol: str
    signal: str
    confidence: float
    entry: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    risk_reward: float
    trend: str
    rsi: float
    macd: float
    atr: float
    support: float
    resistance: float
    ai_summary: str
