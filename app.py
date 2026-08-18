import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import sys

st.set_page_config(page_title="Mutual Fund Analytics Platform", layout="wide")

st.title("Mutual Fund Analytics Platform")
st.caption("Bluestock Fintech Capstone | Dynamic Data Pipeline & Analytics Engine")

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
from etl_pipeline import generate_dynamic_data

@st.cache_data
def get_data():
    return generate_dynamic_data()

df_funds, df_nav, df_aum, df_sip, df_txns = get_data()

tabs = st.tabs(["Market Overview", "Fund Performance & Risk", "Investor Demographics"])

with tabs[0]:
    st.subheader("Industry AUM & Monthly SIP Inflow Milestone")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SBI MF AUM", "INR 12.5L Cr", "+18% YoY")
    c2.metric("Dec 2025 SIP Inflow", "INR 31,002 Cr", "Record Peak")
    c3.metric("Industry Folios", "26.12 Cr", "2.0x Growth")
    c4.metric("Active Schemes", f"{len(df_funds)} Schemes", "10 Top AMCs")
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_sip = px.line(df_sip, x="month_year", y="sip_inflow_cr", title="Monthly SIP Inflow Trajectory (INR Crores)", markers=True)
        st.plotly_chart(fig_sip, use_container_width=True)
    with col_b:
        fig_aum = px.bar(df_aum[df_aum["quarter"] == "Q4 2025"], x="amc_name", y="aum_crores", title="AMC AUM Distribution (Q4 2025 INR Cr)", color="aum_crores")
        st.plotly_chart(fig_aum, use_container_width=True)

with tabs[1]:
    st.subheader("Fund Performance & Scheme Distribution")
    fig_funds = px.bar(df_funds, x="expense_ratio", y="scheme_name", color="amc_name", orientation="h", title="Expense Ratio across AMC Direct Growth Schemes")
    st.plotly_chart(fig_funds, use_container_width=True)

with tabs[2]:
    st.subheader("Demographic & State Transaction Breakdown")
    col_e, col_f = st.columns(2)
    with col_e:
        fig_state = px.histogram(df_txns, x="state", color="txn_type", title="Transaction Count by Indian State & Type")
        st.plotly_chart(fig_state, use_container_width=True)
    with col_f:
        fig_tier = px.pie(df_txns, names="city_tier", title="Transactions by City Tier Tier 1 vs Tier 2")
        st.plotly_chart(fig_tier, use_container_width=True)
