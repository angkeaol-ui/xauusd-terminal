import pandas as pd


def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line


def calculate_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift(1)).abs()
    low_close = (df["low"] - df["close"].shift(1)).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(period).mean()


def find_support_resistance(df):
    recent = df.tail(30)
    support = recent["low"].min()
    resistance = recent["high"].max()
    return float(support), float(resistance)


def generate_signal(df):
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
            "ai_summary": "No data available"
        }

    df = df.copy()
    df["ema_fast"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=200, adjust=False).mean()
    df["rsi"] = calculate_rsi(df["close"], 14)
    macd, signal_line = calculate_macd(df["close"], 12, 26, 9)
    df["macd"] = macd
    df["macd_signal"] = signal_line
    df["atr"] = calculate_atr(df, 14)

    latest = df.iloc[-1]
    trend = "bullish" if latest["ema_fast"] > latest["ema_slow"] and latest["ema_slow"] > latest["ema_long"] else "bearish" if latest["ema_fast"] < latest["ema_slow"] and latest["ema_slow"] < latest["ema_long"] else "neutral"

    rsi = float(latest["rsi"])
    macd_value = float(latest["macd"] - latest["macd_signal"])
    atr = float(latest["atr"]) if not pd.isna(latest["atr"]) else 0.0
    support, resistance = find_support_resistance(df)

    if trend == "bullish" and rsi > 50 and macd_value > 0:
        signal = "BUY"
    elif trend == "bearish" and rsi < 50 and macd_value < 0:
        signal = "SELL"
    else:
        signal = "HOLD"

    price = float(latest["close"])
    if signal == "BUY":
        entry = price
        stop_loss = entry - (atr * 1.2)
        tp1 = entry + (atr * 2.1)
        tp2 = entry + (atr * 3.2)
    elif signal == "SELL":
        entry = price
        stop_loss = entry + (atr * 1.2)
        tp1 = entry - (atr * 2.1)
        tp2 = entry - (atr * 3.2)
    else:
        entry = price
        stop_loss = price - (atr * 1.1)
        tp1 = price + (atr * 1.6)
        tp2 = price + (atr * 2.4)

    risk_reward = abs((tp1 - entry) / (entry - stop_loss)) if signal in ["BUY", "SELL"] and abs(entry - stop_loss) > 0 else 1.0

    confidence = 0.65
    if signal == "BUY" and trend == "bullish":
        confidence = 0.72
    if signal == "SELL" and trend == "bearish":
        confidence = 0.72
    if signal == "HOLD":
        confidence = 0.58

    ai_summary = (
        f"Gold is {trend} based on EMA structure and momentum. "
        f"RSI is {rsi:.1f} and MACD is {macd_value:.2f}, "
        f"with support around {support:.2f} and resistance near {resistance:.2f}. "
        f"The current setup favors a {signal.lower()} bias with a confidence of {confidence * 100:.0f}%."
    )

    return {
        "symbol": "XAUUSD",
        "signal": signal,
        "confidence": round(confidence, 2),
        "entry": round(entry, 2),
        "stop_loss": round(stop_loss, 2),
        "take_profit_1": round(tp1, 2),
        "take_profit_2": round(tp2, 2),
        "risk_reward": round(risk_reward, 2),
        "trend": trend,
        "rsi": round(float(rsi), 2),
        "macd": round(float(macd_value), 2),
        "atr": round(float(atr), 2),
        "support": round(float(support), 2),
        "resistance": round(float(resistance), 2),
        "ai_summary": ai_summary
    }
