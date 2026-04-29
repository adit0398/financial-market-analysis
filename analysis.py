"""
analysis.py
-----------
Pandas-based EDA and analytics pipeline for stock market data.
Reads raw_market_data.csv and produces analysis_output.csv.

Metrics computed:
  - Daily % Return
  - 7-day & 30-day Simple Moving Average (SMA)
  - 14-day Relative Strength Index (RSI)
  - Bollinger Bands (20-day, 2 std dev)
  - Daily Value Traded (Close x Volume)
  - Monthly Summary (mean close, total volume, monthly return)
"""

import pandas as pd
import numpy as np

# ── Load ───────────────────────────────────────────────────────────────────────
df = pd.read_csv("raw_market_data.csv", parse_dates=["Date"])
df.sort_values(["Ticker", "Date"], inplace=True)
df.reset_index(drop=True, inplace=True)

print("=== Dataset Overview ===")
print(df.info())
print("\nNull values:\n", df.isnull().sum())
print("\nDescriptive Stats:\n", df[["Open","High","Low","Close","Volume"]].describe().round(2))

# ── Feature Engineering ────────────────────────────────────────────────────────
def compute_rsi(series, period=14):
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

grp = df.groupby("Ticker", group_keys=False)

df["Daily_Return_Pct"]  = grp["Close"].transform(lambda x: x.pct_change() * 100).round(4)
df["SMA_7"]             = grp["Close"].transform(lambda x: x.rolling(7).mean()).round(2)
df["SMA_30"]            = grp["Close"].transform(lambda x: x.rolling(30).mean()).round(2)
df["RSI_14"]            = grp["Close"].transform(lambda x: compute_rsi(x, 14)).round(2)

bb_mid   = grp["Close"].transform(lambda x: x.rolling(20).mean())
bb_std   = grp["Close"].transform(lambda x: x.rolling(20).std())
df["BB_Upper"]          = (bb_mid + 2 * bb_std).round(2)
df["BB_Lower"]          = (bb_mid - 2 * bb_std).round(2)
df["BB_Mid"]            = bb_mid.round(2)

df["Value_Traded_Cr"]   = (df["Close"] * df["Volume"] / 1e7).round(2)  # in Crores

# ── Monthly Summary ────────────────────────────────────────────────────────────
df["YearMonth"] = df["Date"].dt.to_period("M")

monthly = (
    df.groupby(["Ticker", "YearMonth"])
    .agg(
        Avg_Close    = ("Close", "mean"),
        Max_Close    = ("Close", "max"),
        Min_Close    = ("Close", "min"),
        Total_Volume = ("Volume", "sum"),
        Avg_RSI      = ("RSI_14", "mean"),
    )
    .round(2)
    .reset_index()
)

# Monthly return = (last close - first close) / first close
monthly_ret = (
    df.groupby(["Ticker", "YearMonth"])["Close"]
    .agg(lambda x: round((x.iloc[-1] - x.iloc[0]) / x.iloc[0] * 100, 2))
    .reset_index()
    .rename(columns={"Close": "Monthly_Return_Pct"})
)
monthly = monthly.merge(monthly_ret, on=["Ticker", "YearMonth"])

# ── Correlation Matrix (Close prices) ─────────────────────────────────────────
pivot = df.pivot(index="Date", columns="Ticker", values="Close")
corr  = pivot.corr().round(4)

print("\n=== Close Price Correlation Matrix ===")
print(corr)

# ── Volatility Summary ────────────────────────────────────────────────────────
volatility = (
    df.groupby("Ticker")["Daily_Return_Pct"]
    .agg(Annualised_Volatility=lambda x: round(x.std() * np.sqrt(252), 4))
    .reset_index()
)
print("\n=== Annualised Volatility ===")
print(volatility)

# ── Save Outputs ───────────────────────────────────────────────────────────────
df.drop(columns=["YearMonth"]).to_csv("analysis_output.csv", index=False)
monthly.to_csv("monthly_summary.csv", index=False)
corr.to_csv("correlation_matrix.csv")
volatility.to_csv("volatility_summary.csv", index=False)

print("\nOutputs saved:")
print("  analysis_output.csv")
print("  monthly_summary.csv")
print("  correlation_matrix.csv")
print("  volatility_summary.csv")
