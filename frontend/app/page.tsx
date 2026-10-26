"use client";

import { useEffect, useState } from "react";

type Signal = {
  symbol: string;
  signal: string;
  confidence: number;
  entry: number;
  stop_loss: number;
  take_profit_1: number;
  take_profit_2: number;
  risk_reward: number;
  trend: string;
  rsi: number;
  macd: number;
  atr: number;
  support: number;
  resistance: number;
  ai_summary: string;
};

export default function HomePage() {
  const [signal, setSignal] = useState<Signal | null>(null);
  const [market, setMarket] = useState<any>(null);
  const [timeframe, setTimeframe] = useState("1M");

  const fetchData = async () => {
    try {
      const marketRes = await fetch(`http://localhost:8000/api/market/xauusd?timeframe=${timeframe}`);
      const marketData = await marketRes.json();
      setMarket(marketData);

      const signalRes = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ timeframe })
      });
      const signalData = await signalRes.json();
      setSignal(signalData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [timeframe]);

  const price = market?.price ?? 0;
  const changePercent = market?.change_percent ?? 0;

  return (
    <main className="page-shell">
      <div className="terminal-wrap">
        <div className="topbar">
          <div className="pair-label">XAUUSD</div>
          <div className="timeframe-row">
            {["1M", "1H", "4H", "1D"].map((tf) => (
              <button
                key={tf}
                className={timeframe === tf ? "time-pill active" : "time-pill"}
                onClick={() => setTimeframe(tf)}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>

        <div className="price-panel">
          <div className="price-row">
            <div>
              <div className="small-label">Gold Spot / USD</div>
              <div className="price-value">{price.toFixed(2)}</div>
            </div>

            <div className={changePercent >= 0 ? "change positive" : "change negative"}>
              {changePercent >= 0 ? "+" : ""}
              {changePercent.toFixed(2)}%
            </div>
          </div>

          <div className="chart-box">
            <div className="chart-grid">
              {Array.from({ length: 34 }).map((_, i) => {
                const height = 28 + ((i * 9) % 90);
                const isBull = i % 2 === 0;
                return (
                  <div
                    key={i}
                    className={isBull ? "bar bull" : "bar bear"}
                    style={{ height: `${height}px` }}
                  />
                );
              })}
            </div>
          </div>

          {signal && (
            <div className="signal-card">
              <div className="signal-header">
                <div className={`signal-badge ${signal.signal.toLowerCase()}`}>
                  {signal.signal}
                </div>
                <div className="signal-meta">
                  <div className="signal-label">Model Confidence</div>
                  <div className="signal-confidence">{(signal.confidence * 100).toFixed(0)}%</div>
                </div>
                <div className="signal-meta right">
                  <div className="signal-label">Risk/Reward</div>
                  <div className="signal-confidence">{signal.risk_reward.toFixed(2)}</div>
                </div>
              </div>

              <div className="trade-grid">
                <div className="metric-box">
                  <div className="metric-label">Entry</div>
                  <div className="metric-value">{signal.entry.toFixed(2)}</div>
                </div>

                <div className="metric-box">
                  <div className="metric-label">Stop Loss</div>
                  <div className="metric-value">{signal.stop_loss.toFixed(2)}</div>
                </div>

                <div className="metric-box">
                  <div className="metric-label">Take Profit 1</div>
                  <div className="metric-value">{signal.take_profit_1.toFixed(2)}</div>
                </div>

                <div className="metric-box">
                  <div className="metric-label">Take Profit 2</div>
                  <div className="metric-value">{signal.take_profit_2.toFixed(2)}</div>
                </div>
              </div>

              <div className="indicator-panel">
                <div className="indicator-row">
                  <div className="indicator-box">
                    <div className="metric-label">RSI (14)</div>
                    <div className="indicator-value">{signal.rsi.toFixed(1)}</div>
                  </div>

                  <div className="indicator-box">
                    <div className="metric-label">MACD</div>
                    <div className="indicator-value">{signal.macd.toFixed(2)}</div>
                  </div>
                </div>

                <div className="indicator-row">
                  <div className="indicator-box">
                    <div className="metric-label">ATR</div>
                    <div className="indicator-value">{signal.atr.toFixed(2)}</div>
                  </div>

                  <div className="indicator-box">
                    <div className="metric-label">Trend</div>
                    <div className="indicator-value">{signal.trend}</div>
                  </div>
                </div>
              </div>

              <div className="summary-box">
                <div className="summary-title">AI Summary</div>
                <div className="summary-text">{signal.ai_summary}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
