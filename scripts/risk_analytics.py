import os
import pandas as pd
import numpy as np

def compute_risk_metrics():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    df_perf = pd.read_csv(os.path.join(data_dir, "07_scheme_performance.csv"))
    
    # 1. Sharpe Ranks
    df_sharpe = df_perf[["scheme_code", "scheme_name", "sharpe_ratio", "sortino_ratio"]].sort_values(by="sharpe_ratio", ascending=False)
    df_sharpe.to_csv(os.path.join(data_dir, "fund_sharpe_ranks.csv"), index=False)
    
    # 2. VaR and Drawdown Summary
    df_var = df_perf[["scheme_code", "scheme_name", "max_drawdown", "std_dev"]].copy()
    df_var["var_95"] = np.round(df_var["std_dev"] * 1.645, 2)
    df_var.to_csv(os.path.join(data_dir, "var_drawdown_summary.csv"), index=False)
    
    # 3. Alpha Beta Table
    df_ab = df_perf[["scheme_code", "scheme_name", "alpha", "beta"]].sort_values(by="alpha", ascending=False)
    df_ab.to_csv(os.path.join(data_dir, "alpha_beta_table.csv"), index=False)
    
    print("Risk analytics computed and exported to CSV files.")

if __name__ == "__main__":
    compute_risk_metrics()
