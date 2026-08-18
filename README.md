# Mutual Fund Analytics Platform

Capstone Project | Bluestock Fintech Pvt. Ltd.

An end to end data engineering and analytics platform built using publicly available Indian mutual fund data from AMFI India and mfapi.in API interfaces. The pipeline extracts, cleans, and transforms raw NAV history, quarterly AUM, and investor transaction data dynamically, loading into a 5+ table Star Schema database.

## Project Documentation & Technical Report

* **Download PDF Technical Report**: [Technical_Report_Mutual_Fund_Analytics.pdf](Technical_Report_Mutual_Fund_Analytics.pdf)
* **Star Schema DDL**: [sql/schema.sql](sql/schema.sql)
* **Dynamic ETL Pipeline Script**: [scripts/etl_pipeline.py](scripts/etl_pipeline.py)

## Key Industry Benchmarks

* **Monthly SIP Inflow Peak**: INR 31,002 Cr milestone (Dec 2025)
* **SBI MF AUM Anchor**: INR 12.5L Cr
* **Industry Folios**: Growth from 13.26 Cr to 26.12 Cr
* **Dynamic Processing**: Automated data pipeline ingesting 40 AMFI scheme codes, 46,000+ daily NAV records, and investor transactions across Indian states

## Quickstart Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Execute Dynamic ETL Pipeline
```bash
python scripts/etl_pipeline.py
```

### 3. Launch Interactive Analytics Dashboard
```bash
streamlit run app.py
```
