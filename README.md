# Mutual Fund Analytics Platform

Capstone Project | Bluestock Fintech Pvt. Ltd.

An end to end data engineering and analytics platform built using publicly available Indian mutual fund data from AMFI India and mfapi.in. The platform extracts raw daily NAV, quarterly AUM, and investor transaction data, loads it into a normalized 5+ table Star Schema database, and provides interactive risk and performance dashboards.

## Project Documentation & Technical Report

* **Download PDF Technical Report**: [Technical_Report_Mutual_Fund_Analytics.pdf](Technical_Report_Mutual_Fund_Analytics.pdf)
* **Star Schema DDL**: [sql/schema.sql](sql/schema.sql)
* **ETL Pipeline Script**: [scripts/etl_pipeline.py](scripts/etl_pipeline.py)
* **Risk Analytics Engine**: [scripts/risk_analytics.py](scripts/risk_analytics.py)

## Key Industry Benchmarks

* **Monthly SIP Inflow Peak**: INR 31,002 Cr milestone (Dec 2025)
* **SBI MF AUM Anchor**: INR 12.5L Cr
* **Industry Folios**: Growth from 13.26 Cr to 26.12 Cr
* **Dataset Scale**: 40 AMFI scheme codes, 46,000+ daily NAV records, 32,000+ transactions across 5,000 investors in 12 Indian states

## 10 Provided Datasets

1. `01_fund_master.csv`: 40 AMFI schemes across 10 top AMCs
2. `02_nav_history.csv`: 46,000+ daily NAV records (Jan 2022 to May 2026)
3. `03_aum_by_fund_house.csv`: Quarterly AUM for top 10 AMCs
4. `04_monthly_sip_inflows.csv`: Monthly SIP inflows peaking at INR 31,002 Cr
5. `05_category_inflows.csv`: Category wise net inflows for FY 2024 to 2025
6. `06_industry_folio_count.csv`: Total industry folios timeline
7. `07_scheme_performance.csv`: CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown
8. `08_investor_transactions.csv`: 32,000+ investor transactions across 12 states
9. `09_portfolio_holdings.csv`: Top stock and sector holdings per equity fund
10. `10_benchmark_indices.csv`: Daily close for Nifty 50, Nifty 100, BSE SmallCap

## Quickstart Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Execute ETL Pipeline & Risk Analytics
```bash
python scripts/etl_pipeline.py
python scripts/risk_analytics.py
```

### 3. Launch Interactive Analytics Dashboard
```bash
streamlit run app.py
```
