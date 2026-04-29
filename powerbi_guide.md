# Power BI Dashboard Guide — Financial Market Analysis

## Step 1 — Import Data
1. Open Power BI Desktop
2. Home → Get Data → Text/CSV → select `analysis_output.csv`
3. Repeat for `monthly_summary.csv` and `volatility_summary.csv`
4. Click Transform Data to open Power Query

## Step 2 — Power Query Transformations
In Power Query for `analysis_output`:
- Change `Date` column → Data Type: Date
- Change `Close`, `Open`, `High`, `Low` → Decimal Number
- Change `Volume`, `Value_Traded_Cr` → Whole Number / Decimal
- Close & Apply

## Step 3 — Data Model (Relationships)
No relationships needed — Ticker and Date are repeated in each table.
Use slicers to filter all visuals simultaneously.

## Step 4 — DAX Measures
In the Data pane, create a new table called **Measures** and add:

```dax
// Total Value Traded
Total Value Traded = SUM(analysis_output[Value_Traded_Cr])

// Average RSI
Avg RSI = AVERAGE(analysis_output[RSI_14])

// Average Daily Return
Avg Daily Return % = AVERAGE(analysis_output[Daily_Return_Pct])

// Latest Close Price
Latest Close = 
CALCULATE(
    MAX(analysis_output[Close]),
    analysis_output[Date] = MAX(analysis_output[Date])
)

// Price Change % (full period)
Total Return % = 
VAR first_close = CALCULATE(MIN(analysis_output[Close]), ALLEXCEPT(analysis_output, analysis_output[Ticker]))
VAR last_close  = CALCULATE(MAX(analysis_output[Close]), ALLEXCEPT(analysis_output, analysis_output[Ticker]))
RETURN DIVIDE(last_close - first_close, first_close) * 100
```

## Step 5 — Visuals to Build

| Page         | Visual                    | Fields                                        |
|-------------|---------------------------|-----------------------------------------------|
| Overview    | Card                      | Latest Close, Total Return %, Avg RSI         |
| Overview    | Line Chart                | Date (X), Close (Y), Ticker (Legend)          |
| Overview    | Slicer                    | Ticker                                        |
| Performance | Clustered Bar             | Ticker (X), Monthly_Return_Pct (Y)            |
| Performance | Line Chart                | YearMonth (X), Avg_Close (Y), Ticker (Legend) |
| Risk        | Clustered Bar             | Ticker, Annualised_Volatility                 |
| Risk        | Scatter Chart             | Annualised_Volatility (X), Total Return % (Y) |
| Indicators  | Line Chart (multi-series) | Date (X), RSI_14, SMA_7, SMA_30 (Y)          |
| Indicators  | Area Chart                | Date (X), BB_Upper, BB_Mid, BB_Lower (Y)      |

## Step 6 — Formatting Tips
- Theme: "Executive" or "Innovate" (View → Themes)
- Add a Text Box title to each page
- Set all Date slicers to "Between" filter type
- Format Currency fields: INR prefix (₹), 0 decimal for price, 2 for return %

## Step 7 — Publish
File → Publish → Select your Power BI Workspace
