-- sql/schema.sql
-- Star Schema DDL Design for Bluestock MF Capstone

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    date TEXT,
    amfi_code INTEGER,
    nav REAL,
    PRIMARY KEY (date, amfi_code),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id TEXT,
    amfi_code INTEGER,
    transaction_date TEXT,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
