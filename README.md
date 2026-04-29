# Financial Market Analysis Dashboard

**Tech Stack:** Python | NumPy | Pandas | openpyxl (Advanced Excel) | Power BI

## Project Structure

```
financial_market_analysis/
├── data_generator.py        ← Step 1: Synthetic OHLCV data (NumPy GBM simulation)
├── analysis.py              ← Step 2: EDA + technical indicators (Pandas)
├── excel_dashboard.py       ← Step 3: 6-sheet Excel dashboard (openpyxl)
├── powerbi_guide.md         ← Step 4: Power BI setup & DAX measures
└── README.md
```

## How to Run

### Prerequisites
```bash
pip install pandas numpy openpyxl
```

### Run in order

```bash
# 1. Generate synthetic market data
python data_generator.py
# → raw_market_data.csv (2,520 rows × 7 columns)

# 2. Run EDA and compute indicators
python analysis.py
# → analysis_output.csv   (2,520 rows with 15 columns)
# → monthly_summary.csv   (monthly KPIs per ticker)
# → correlation_matrix.csv
# → volatility_summary.csv

# 3. Build Excel dashboard
python excel_dashboard.py
# → financial_market_dashboard.xlsx (6 sheets)

# 4. Power BI
# Open Power BI Desktop and follow powerbi_guide.md
```

## What It Does

### data_generator.py — NumPy
- Simulates 2 years of daily OHLCV data for 5 NSE stocks
- Uses **Geometric Brownian Motion** (industry-standard price model)
- Generates realistic Volume spikes on high-volatility days

### analysis.py — Pandas
- Cleans and validates data (null checks, type enforcement)
- Computes: **SMA-7, SMA-30, RSI-14, Bollinger Bands, Value Traded**
- Produces monthly aggregations and annualised volatility
- Outputs **correlation matrix** across all tickers

### excel_dashboard.py — openpyxl (Advanced Excel)
| Sheet           | Content                                              |
|----------------|------------------------------------------------------|
| Raw Data        | Full OHLCV + indicators with conditional formatting  |
| Monthly Summary | Per-ticker monthly KPIs with colour scale            |
| Price Chart     | Multi-series line chart of closing prices            |
| RSI Chart       | RSI trend with 0–100 axis and overbought zones       |
| Volatility      | Annualised volatility bar chart                      |
| Correlation     | Heatmap-style correlation matrix                     |

### Power BI
- 4-page interactive report
- DAX measures for Total Return, Avg RSI, Latest Price
- Slicer-driven filtering by ticker and date range

## Dataset Details
- **Companies:** RELIANCE, TCS, INFY, HDFCBANK, WIPRO (synthetic, not real)
- **Period:** Jan 2023 – Dec 2024 (~504 trading days)
- **Rows:** 2,520 (504 days × 5 tickers)
