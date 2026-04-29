"""
data_generator.py
-----------------
Generates synthetic stock market data for 5 companies over 2 years
using NumPy's random simulation (Geometric Brownian Motion model).

Output: raw_market_data.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────────
COMPANIES = {
    "RELIANCE": {"start_price": 2400, "mu": 0.0003,  "sigma": 0.018},
    "TCS":      {"start_price": 3500, "mu": 0.00025, "sigma": 0.015},
    "INFY":     {"start_price": 1500, "mu": 0.00028, "sigma": 0.016},
    "HDFCBANK": {"start_price": 1600, "mu": 0.00022, "sigma": 0.014},
    "WIPRO":    {"start_price": 400,  "mu": 0.00020, "sigma": 0.020},
}

START_DATE = datetime(2023, 1, 2)
TRADING_DAYS = 504   # ~2 years of trading days


def generate_price_series(start_price, mu, sigma, n):
    """Geometric Brownian Motion price simulation."""
    daily_returns = np.random.normal(mu, sigma, n)
    price_relatives = np.exp(daily_returns)
    prices = start_price * np.cumprod(price_relatives)
    return np.round(prices, 2)


def generate_ohlcv(close_prices):
    """Generate Open, High, Low, Volume from Close prices."""
    n = len(close_prices)

    open_prices = np.round(close_prices * (1 + np.random.uniform(-0.005, 0.005, n)), 2)
    high_prices = np.round(np.maximum(close_prices, open_prices) + np.abs(np.random.normal(0, 15, n)), 2)
    low_prices  = np.round(np.minimum(close_prices, open_prices) - np.abs(np.random.normal(0, 10, n)), 2)
    low_prices  = np.clip(low_prices, 1, None)

    pct_change  = np.abs(np.diff(close_prices, prepend=close_prices[0]) / close_prices)
    base_volume = np.random.randint(800_000, 5_000_000, n)
    volume      = np.round(base_volume * (1 + pct_change * 10)).astype(int)

    return pd.DataFrame({
        "Open": open_prices, "High": high_prices,
        "Low": low_prices,   "Close": close_prices,
        "Volume": volume,
    })


def generate_trading_dates(start, n):
    dates, current = [], start
    while len(dates) < n:
        if current.weekday() < 5:
            dates.append(current)
        current += timedelta(days=1)
    return pd.DatetimeIndex(dates)


def main():
    dates = generate_trading_dates(START_DATE, TRADING_DAYS)
    all_rows = []
    for ticker, cfg in COMPANIES.items():
        close_prices = generate_price_series(cfg["start_price"], cfg["mu"], cfg["sigma"], TRADING_DAYS)
        ohlcv = generate_ohlcv(close_prices)
        ohlcv.insert(0, "Date",   dates.strftime("%Y-%m-%d"))
        ohlcv.insert(1, "Ticker", ticker)
        all_rows.append(ohlcv)

    df = pd.concat(all_rows, ignore_index=True)
    df.to_csv("raw_market_data.csv", index=False)
    print(f"raw_market_data.csv generated — {len(df):,} rows x {df.shape[1]} columns")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
