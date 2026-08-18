import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Mutual Fund Analytics Platform", layout="wide")

st.title("Mutual Fund Analytics Platform")
st.caption("Bluestock Fintech Capstone | End to End Data Engineering & Analytics")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    df_funds = pd.read_csv(os.path.join(data_dir, "01_fund_master.csv"))
    df_aum = pd.read_csv(os.path.join(data_dir, "03_aum_by_fund_house.csv"))
    df_sip = pd.read_csv(os.path.join(data_dir, "04_monthly_sip_inflows.csv"))
    df_perf = pd.read_csv(os.path.join(data_dir, "07_scheme_performance.csv"))
    df_txns = pd.read_csv(os.path.join(data_dir, "08_investor_transactions.csv"))
    df_holdings = pd.read_csv(os.path.join(data_dir, "09_portfolio_holdings.csv"))
    
    return df_funds, df_aum, df_sip, df_perf, df_txns, df_holdings

df_funds, df_aum, df_sip, df_perf, df_txns, df_holdings = load_data()

tabs = st.tabs(["Market Overview", "Fund Performance & Risk", "Investor Demographics", "Portfolio Holdings"])

# Page 1: Market Overview
with tabs[0]:
    st.subheader("Industry AUM & Monthly SIP Inflow Milestone")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SBI MF AUM", "INR 12.5L Cr", "+18% YoY")
    c2.metric("Dec 2025 SIP Inflow", "INR 31,002 Cr", "Record Peak")
    c3.metric("Industry Folios", "26.12 Cr", "2.0x Growth")
    c4.metric("Active Schemes", "40 Schemes", "10 Top AMCs")
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_sip = px.line(df_sip, x="month_year", y="sip_inflow_cr", title="Monthly SIP Inflow Trajectory (INR Crores)", markers=True)
        st.plotly_chart(fig_sip, use_container_width=True)
    with col_b:
        fig_aum = px.bar(df_aum[df_aum["quarter"] == "Q4 2025"], x="amc_name", y="aum_crores", title="AMC AUM Distribution (Q4 2025 INR Cr)", color="aum_crores")
        st.plotly_chart(fig_aum, use_container_width=True)

# Page 2: Fund Performance & Risk
with tabs[1]:
    st.subheader("Risk & Return Metrics Analysis")
    fig_scatter = px.scatter(df_perf, x="sharpe_ratio", y="sortino_ratio", color="alpha", size="cagr_3yr", hover_name="scheme_name", title="Sharpe vs Sortino Ratio Matrix")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    col_c, col_d = st.columns(2)
    with col_c:
        fig_alpha = px.bar(df_perf.sort_values(by="alpha", ascending=False).head(10), x="alpha", y="scheme_name", orientation="h", title="Top 10 Funds by Jensen Alpha Generation")
        st.plotly_chart(fig_alpha, use_container_width=True)
    with col_d:
        fig_dd = px.bar(df_perf.sort_values(by="max_drawdown").head(10), x="max_drawdown", y="scheme_name", orientation="h", title="Lowest Maximum Drawdown (%)")
        st.plotly_chart(fig_dd, use_container_width=True)

# Page 3: Investor Demographics
with tabs[2]:
    st.subheader("Demographic & State Transaction Breakdown")
    col_e, col_f = st.columns(2)
    with col_e:
        fig_state = px.histogram(df_txns, x="state", color="txn_type", title="Transaction Count by Indian State & Type")
        st.plotly_chart(fig_state, use_container_width=True)
    with col_f:
        fig_tier = px.pie(df_txns, names="city_tier", title="Transactions by City Tier Tier 1 vs Tier 2 vs Tier 3")
        st.plotly_chart(fig_tier, use_container_width=True)

# Page 4: Portfolio Holdings
with tabs[3]:
    st.subheader("Top Stock & Sector Concentrations")
    fig_sec = px.sunburst(df_holdings, path=["sector", "stock_name"], values="weight_pct", title="Stock & Sector Concentration Hierarchy")
    st.plotly_chart(fig_sec, use_container_width=True)
