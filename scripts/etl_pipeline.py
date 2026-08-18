import os
import pandas as pd
import sqlite3

def run_etl():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    db_path = os.path.join(base_dir, "mutual_funds.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Run Schema DDL
    with open(os.path.join(base_dir, "sql", "schema.sql"), "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
        
    # 1. Load Fund Master
    df_funds = pd.read_csv(os.path.join(data_dir, "01_fund_master.csv"))
    df_funds.to_sql("dim_fund", conn, if_exists="replace", index=False)
    
    # 2. Load NAV History
    df_nav = pd.read_csv(os.path.join(data_dir, "02_nav_history.csv"))
    df_nav.to_sql("fact_nav", conn, if_exists="replace", index=False)
    
    # 3. Load AUM
    df_aum = pd.read_csv(os.path.join(data_dir, "03_aum_by_fund_house.csv"))
    df_aum.to_sql("fact_aum", conn, if_exists="replace", index=False)
    
    # 4. Load SIP
    df_sip = pd.read_csv(os.path.join(data_dir, "04_monthly_sip_inflows.csv"))
    df_sip.to_sql("fact_sip", conn, if_exists="replace", index=False)
    
    # 5. Load Transactions & Investors
    df_txns = pd.read_csv(os.path.join(data_dir, "08_investor_transactions.csv"))
    df_investors = df_txns[["investor_id", "state", "city_tier", "investor_age", "income_bracket"]].drop_duplicates("investor_id")
    df_investors.to_sql("dim_investor", conn, if_exists="replace", index=False)
    
    df_fact_txns = df_txns[["txn_id", "investor_id", "scheme_code", "txn_type", "amount_inr", "txn_date"]]
    df_fact_txns.to_sql("fact_transactions", conn, if_exists="replace", index=False)
    
    conn.commit()
    conn.close()
    print("ETL pipeline executed successfully. Star schema loaded into SQLite.")

if __name__ == "__main__":
    run_etl()
