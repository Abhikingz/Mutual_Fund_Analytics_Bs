-- Bluestock Fintech Mutual Fund Star Schema DDL (5+ Tables)

CREATE TABLE IF NOT EXISTS dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    amc_name TEXT NOT NULL,
    category TEXT NOT NULL,
    expense_ratio REAL,
    benchmark TEXT,
    fund_manager TEXT,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    nav_date DATE NOT NULL,
    nav_value REAL NOT NULL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amc_name TEXT NOT NULL,
    quarter TEXT NOT NULL,
    aum_crores REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sip (
    sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month_year TEXT NOT NULL,
    sip_inflow_cr REAL NOT NULL,
    active_accounts_crore REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_investor (
    investor_id TEXT PRIMARY KEY,
    state TEXT,
    city_tier TEXT,
    investor_age INTEGER,
    income_bracket TEXT
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_id TEXT PRIMARY KEY,
    investor_id TEXT,
    scheme_code INTEGER,
    txn_type TEXT,
    amount_inr REAL,
    txn_date DATE,
    FOREIGN KEY (investor_id) REFERENCES dim_investor(investor_id),
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);
