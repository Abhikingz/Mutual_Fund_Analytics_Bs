import os
import pandas as pd
import numpy as np
import sqlite3

def generate_dynamic_data():
    amcs = ["SBI MF", "HDFC MF", "ICICI Prudential", "Nippon India", "Kotak", "Axis", "Aditya Birla Sun Life", "UTI", "Mirae Asset", "DSP MF"]
    categories = ["Large Cap", "Mid Cap", "Small Cap", "ELSS", "Flexi Cap", "Liquid", "Gilt", "Multi Cap"]
    
    # 1. Fund Master
    schemes = []
    np.random.seed(42)
    for i in range(1, 41):
        amc = amcs[(i - 1) % len(amcs)]
        cat = categories[(i - 1) % len(categories)]
        schemes.append({
            "scheme_code": 120000 + i * 123,
            "scheme_name": f"{amc} {cat} Direct Growth",
            "amc_name": amc,
            "category": cat,
            "expense_ratio": round(float(np.random.uniform(0.35, 1.25)), 2),
            "benchmark": "Nifty 50",
            "fund_manager": "Fund Manager",
            "risk_grade": np.random.choice(["Very High", "High", "Moderate"])
        })
    df_funds = pd.DataFrame(schemes)
    
    # 2. NAV History
    dates = pd.date_range(start="2022-01-01", end="2026-05-31", freq="B")
    nav_records = []
    for s in schemes:
        base_nav = float(np.random.uniform(25.0, 150.0))
        returns = np.random.normal(0.0004, 0.011, len(dates))
        navs = base_nav * np.exp(np.cumsum(returns))
        for d, val in zip(dates, navs):
            nav_records.append({
                "scheme_code": s["scheme_code"],
                "nav_date": d.strftime("%Y-%m-%d"),
                "nav_value": round(float(val), 4)
            })
    df_nav = pd.DataFrame(nav_records)
    
    # 3. AUM History
    quarters = ["Q1 2022", "Q2 2022", "Q3 2022", "Q4 2022", "Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"]
    aum_records = []
    base_aums = [1114000, 680000, 720000, 510000, 480000, 420000, 390000, 310000, 290000, 250000]
    for q in quarters:
        for idx, amc in enumerate(amcs):
            growth = 1 + (quarters.index(q) * 0.015) + np.random.uniform(-0.01, 0.02)
            aum_records.append({"amc_name": amc, "quarter": q, "aum_crores": round(base_aums[idx] * growth, 2)})
    df_aum = pd.DataFrame(aum_records)
    
    # 4. SIP Monthly Inflows
    sip_months = pd.date_range(start="2022-01-01", end="2025-12-01", freq="MS")
    sip_records = []
    for idx, m in enumerate(sip_months):
        sip_val = 31002 if idx == len(sip_months) - 1 else 11500 + (idx * 410)
        sip_records.append({"month_year": m.strftime("%Y-%m"), "sip_inflow_cr": sip_val, "active_accounts_crore": round(13.26 + (idx * 0.27), 2)})
    df_sip = pd.DataFrame(sip_records)
    
    # 5. Transactions
    states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Gujarat", "Uttar Pradesh"]
    txns = []
    for i in range(1, 10001):
        inv_id = (i % 2000) + 1
        txns.append({
            "txn_id": f"TXN-{i:06d}",
            "investor_id": f"INV-{inv_id:05d}",
            "scheme_code": schemes[i % len(schemes)]["scheme_code"],
            "state": states[inv_id % len(states)],
            "city_tier": "Tier 1" if inv_id % 3 == 0 else "Tier 2",
            "investor_age": 25 + (inv_id % 40),
            "income_bracket": "12-25L",
            "txn_type": "SIP" if i % 2 == 0 else "Lumpsum",
            "amount_inr": np.random.randint(2000, 50000),
            "txn_date": "2025-01-15"
        })
    df_txns = pd.DataFrame(txns)
    
    return df_funds, df_nav, df_aum, df_sip, df_txns

def run_etl():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "mutual_funds.db")
    
    df_funds, df_nav, df_aum, df_sip, df_txns = generate_dynamic_data()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(os.path.join(base_dir, "sql", "schema.sql"), "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
        
    df_funds.to_sql("dim_fund", conn, if_exists="replace", index=False)
    df_nav.to_sql("fact_nav", conn, if_exists="replace", index=False)
    df_aum.to_sql("fact_aum", conn, if_exists="replace", index=False)
    df_sip.to_sql("fact_sip", conn, if_exists="replace", index=False)
    
    df_investors = df_txns[["investor_id", "state", "city_tier", "investor_age", "income_bracket"]].drop_duplicates("investor_id")
    df_investors.to_sql("dim_investor", conn, if_exists="replace", index=False)
    
    df_fact_txns = df_txns[["txn_id", "investor_id", "scheme_code", "txn_type", "amount_inr", "txn_date"]]
    df_fact_txns.to_sql("fact_transactions", conn, if_exists="replace", index=False)
    
    conn.commit()
    conn.close()
    print("ETL pipeline generated and loaded Star Schema into SQLite dynamically.")

if __name__ == "__main__":
    run_etl()
