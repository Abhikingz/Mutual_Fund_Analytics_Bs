# scripts/etl_pipeline.py
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# Absolute path configurations
BASE_DIR = Path(r"C:\Users\lenovo\bluestock_mf_capstone")
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_DIR = BASE_DIR / "data" / "db"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

db_path = DB_DIR / "bluestock_mf.db"
engine = create_engine(f"sqlite:///{db_path}")

def get_file_by_keyword(keyword):
    matches = list(RAW_DIR.glob(f"*{keyword}*.csv"))
    if not matches:
        raise FileNotFoundError(f"Missing required dataset matching keyword: '{keyword}'")
    return matches[0]

def clean_and_load():
    print("🧹 Starting ETL Transformation Processing pipeline...\n")
    
    # 1. Clean NAV History (Handle Holidays and Weekends via forward-fill)
    nav_file = get_file_by_keyword("nav_history")
    df_nav = pd.read_csv(nav_file)
    df_nav['date'] = pd.to_datetime(df_nav['date'])
    df_nav = df_nav.sort_values(by=['amfi_code', 'date']).drop_duplicates()
    df_nav = df_nav[df_nav['nav'] > 0]
    
    # Generate complete day timelines for each mutual fund scheme
    imputed_frames = []
    for code, group in df_nav.groupby('amfi_code'):
        group = group.set_index('date')
        full_timeline = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group = group.reindex(full_timeline)
        group['amfi_code'] = code
        group['nav'] = group['nav'].ffill()  # Fill missing weekend/holiday cells
        imputed_frames.append(group.reset_index().rename(columns={'index': 'date'}))
    
    df_nav_clean = pd.concat(imputed_frames, ignore_index=True)
    df_nav_clean.to_csv(PROCESSED_DIR / "nav_history_clean.csv", index=False)
    df_nav_clean.to_sql("fact_nav", engine, if_exists="replace", index=False)
    print(" -> Loaded 'fact_nav' successfully (Holidays forward-filled).")

    # 2. Clean Investor Transactions
    tx_file = get_file_by_keyword("investor_transactions")
    df_tx = pd.read_csv(tx_file)
    df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])
    df_tx['transaction_type'] = df_tx['transaction_type'].str.upper().str.strip()
    
    # Standardize map configurations
    type_map = {'SIP': 'SIP', 'LUMPSUM': 'LUMPSUM', 'REDEMPTION': 'REDEMPTION', 'PURCHASE': 'LUMPSUM'}
    df_tx['transaction_type'] = df_tx['transaction_type'].map(type_map).fillna('SIP')
    df_tx = df_tx[df_tx['amount'] > 0]
    
    df_tx.to_csv(PROCESSED_DIR / "investor_transactions_clean.csv", index=False)
    df_tx.to_sql("fact_transactions", engine, if_exists="replace", index=False)
    print(" -> Loaded 'fact_transactions' successfully (Inflows standardized).")

    # 3. Clean and Load Fund Master Dimension
    master_file = get_file_by_keyword("fund_master")
    df_master = pd.read_csv(master_file)
    df_master.to_csv(PROCESSED_DIR / "fund_master_clean.csv", index=False)
    df_master.to_sql("dim_fund", engine, if_exists="replace", index=False)
    print(" -> Loaded 'dim_fund' reference dimension details successfully.")

    print(f"\n🎉 ETL Pipeline successfully loaded into database: {db_path}")

if __name__ == '__main__':
    clean_and_load()
