Financial Market Analysis

This project simulates stock market data and performs financial analysis using Python. It also includes an interactive Power BI dashboard built on top of the processed data.

Tech Stack
Python
NumPy
Pandas
Power BI
Project Structure
financial_market_analysis/
├── data_generator.py    # Generates synthetic OHLCV data
├── analysis.py          # Performs analysis and computes indicators
├── powerbi_dashboard.pbix  # Power BI dashboard file
└── README.md
How to Run
Install dependencies
pip install pandas numpy
Execute scripts
# Step 1: Generate market data
python data_generator.py
# Output: raw_market_data.csv

# Step 2: Run analysis
python analysis.py
# Outputs:
# - analysis_output.csv
# - monthly_summary.csv
# - correlation_matrix.csv
# - volatility_summary.csv
Power BI Dashboard
Open the powerbi_dashboard.pbix file in Power BI Desktop
Load the generated CSV files if required
Use filters/slicers to explore different stocks and time periods
Overview

The project generates synthetic stock data and analyzes it to extract insights. The dataset is not real but is designed to behave similarly to actual market data.

Data Generation
Simulates 2 years of daily stock data
Covers 5 stocks: RELIANCE, TCS, INFY, HDFCBANK, WIPRO
Uses Geometric Brownian Motion for price simulation
Generates Open, High, Low, Close, and Volume data
Adds realistic volatility behavior
Analysis
Data cleaning and preprocessing
Technical indicators:
Moving Averages (7-day and 30-day)
RSI (Relative Strength Index)
Bollinger Bands
Outputs:
Monthly summaries
Correlation matrix
Annualised volatility
Power BI Dashboard (Built by Me)
Created a multi-page interactive dashboard using Power BI
Visualizes stock trends, volatility, and indicator performance
Includes slicers for filtering by ticker and date range
Tracks key metrics like price trends, RSI, and overall performance
Helps in quick comparison between different stocks
Dataset Details
Time Period: Jan 2023 – Dec 2024
Total Records: 2,520
Type: Synthetic (not real market data)
Purpose
Practice financial data analysis
Work with time-series datasets
Build end-to-end data projects
Combine Python analysis with Power BI visualization