#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Awash Bank Fraud Analytics", layout="wide")

load_dotenv()

# Realistic lists
branches = [
    "Awash Towers Headquarters - Addis Ababa",
    "Bole Branch - Addis Ababa",
    "Kirkos Branch - Addis Ababa",
    "Mexico Square Branch - Addis Ababa",
    "Piassa Branch - Addis Ababa",
    "Merkato Branch - Addis Ababa",
    "Dire Dawa Branch - Dire Dawa",
    "Bahir Dar Branch - Bahir Dar",
    "Mekelle Branch - Mekelle",
    "Jimma Branch - Jimma",
    "Awassa Branch - Awassa",
    "Adama Branch - Adama",
    "Gondar Branch - Gondar",
    "Dessie Branch - Dessie",
    "Harar Branch - Harar",
    "Shashemene Branch - Shashemene",
    "Arba Minch Branch - Arba Minch",
    "Debre Birhan Branch - Debre Birhan"
]

transaction_channels = [
    "AwashBirr Mobile Transfer",
    "ATM Withdrawal",
    "POS Payment",
    "Branch Deposit",
    "Branch Withdrawal",
    "Agent Banking",
    "Bill Payment",
    "Fund Transfer"
]

# FINAL CSS - Clean main background, black checkbox text
st.markdown("""
<style>
    /* Main background - light, no image */
    .stApp {
        background-color: #f8f9fa;
        background-image: none;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #002D72 !important;
        font-weight: bold;
    }

    /* Normal text */
    .stMarkdown p, .stMarkdown div, .stText, .stCaption {
        color: #333333 !important;
        font-size: 16px !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #002D72 !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* ALL form labels - black and bold */
    label {
        color: black !important;
        font-weight: bold !important;
        font-size: 17px !important;
    }

    /* Checkbox label - explicitly black and large */
    .stCheckbox label {
        color: black !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }

    /* Metric cards */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 6px solid #002D72;
    }

    /* Buttons */
    .stButton > button {
        background-color: #002D72;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #333333 !important;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        background-color: white !important;
    }

    /* Metric text */
    .stMetric > label, .stMetric > div[data-testid="stMetricValue"] {
        color: #333333 !important;
    }

    /* Key factors text - dark */
    .stAlert p {
        color: #333333 !important;
        font-weight: bold !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 80px;
        padding: 20px;
        font-size: 18px;
        color: #002D72;
        font-weight: bold;
        border-top: 2px solid #002D72;
    }
</style>
""", unsafe_allow_html=True)

# DB Connection
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'awash_analytics'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Load Model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('fraud_model.pkl')
        features = joblib.load('model_features.pkl')
        return model, features
    except Exception as e:
        st.error(f"Model load failed: {e}")
        return None, None

model, expected_features = load_model()
if model is None:
    st.stop()

# Header - ONLY logo and text, NO background image
st.markdown("<div style='text-align: center; margin-bottom: 40px;'>", unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Awash_Bank_Final_logo.jpg/800px-Awash_Bank_Final_logo.jpg", width=220)
st.markdown("<h1 style='color:#002D72;'>🏦 Awash Bank Fraud Detection & Risk Analytics Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color:#555;'>Real-time monitoring and predictive fraud detection system simulating Awash Bank S.C. operations in Ethiopia</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar - no logo
st.sidebar.markdown("<h3 style='color:white; text-align:center;'>Navigation</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("Select Page", ["Overview Dashboard", "Fraud Explorer", "Real-Time Fraud Predictor"], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:white; text-align:center;'>Developed by Aklilu Abera</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:white; text-align:center; font-size:14px;'>Portfolio Project • December 2025</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:white; text-align:center; font-size:14px;'>Built with Python, MySQL, scikit-learn & Streamlit</p>", unsafe_allow_html=True)

conn = get_connection()
if conn is None:
    st.stop()

# === Overview Dashboard ===
if page == "Overview Dashboard":
    st.markdown("<h2 style='color:#002D72; text-align:center;'>🔍 Key Metrics & Insights</h2>", unsafe_allow_html=True)

    metrics_query = """
    SELECT 
        COUNT(*) AS total_transactions,
        SUM(fraud_flag) AS total_fraud,
        AVG(amount_etb) AS avg_amount,
        SUM(CASE WHEN fraud_flag = 1 THEN amount_etb ELSE 0 END) AS fraud_amount_etb
    FROM transactions
    """
    metrics_df = pd.read_sql(metrics_query, conn)
    m = metrics_df.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Transactions", f"{int(m['total_transactions']):,}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Fraud Cases Detected", f"{int(m['total_fraud']):,}", delta=f"{m['total_fraud']/m['total_transactions']*100:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Average Amount (ETB)", f"{m['avg_amount']:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Fraud Amount at Risk (ETB)", f"{m['fraud_amount_etb']:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<h3 style='color:#002D72;'>Fraud Rate by Channel</h3>", unsafe_allow_html=True)
        channel_df = pd.read_sql("""
            SELECT channel, ROUND(SUM(fraud_flag)*100.0/COUNT(*), 2) AS fraud_rate
            FROM transactions GROUP BY channel ORDER BY fraud_rate DESC
        """, conn)

        fig, ax = plt.subplots(figsize=(11,6))
        sns.barplot(data=channel_df, x='channel', y='fraud_rate', palette='Blues_d', ax=ax)
        ax.set_title("Fraud Rate by Channel (%)", fontsize=14)
        ax.set_ylabel("Fraud Rate (%)")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with col_right:
        st.markdown("<h3 style='color:#002D72;'>Top 15 Branches by Fraud Rate</h3>", unsafe_allow_html=True)
        branch_df = pd.read_sql("""
            SELECT c.home_branch, ROUND(SUM(t.fraud_flag)*100.0/COUNT(*), 2) AS fraud_rate
            FROM transactions t JOIN customers c ON t.account_number = c.account_number
            GROUP BY c.home_branch ORDER BY fraud_rate DESC LIMIT 15
        """, conn)

        fig2, ax2 = plt.subplots(figsize=(11,8))
        sns.barplot(data=branch_df, y='home_branch', x='fraud_rate', palette='Greens_d', ax=ax2)
        ax2.set_title("Top Branches by Fraud Rate (%)", fontsize=14)
        ax2.set_xlabel("Fraud Rate (%)")
        st.pyplot(fig2)

# === Fraud Explorer ===
elif page == "Fraud Explorer":
    st.markdown("<h2 style='color:#002D72; text-align:center;'>🔎 Explore & Filter Transactions</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    sel_channels = col1.multiselect("Filter by Channel", options=transaction_channels, default=transaction_channels[:3])
    sel_branches = col2.multiselect("Filter by Home Branch", options=branches)

    base_query = """
        SELECT t.transaction_id, DATE(t.date) AS date, t.amount_etb, t.channel, t.location, t.merchant, 
               CASE WHEN t.fraud_flag = 1 THEN 'Fraud' ELSE 'Normal' END AS status,
               c.home_branch, c.balance_etb
        FROM transactions t
        JOIN customers c ON t.account_number = c.account_number
        WHERE 1=1
    """
    params = []

    if sel_channels:
        base_query += f" AND t.channel IN ({','.join(['%s'] * len(sel_channels))})"
        params.extend(sel_channels)

    if sel_branches:
        base_query += f" AND c.home_branch IN ({','.join(['%s'] * len(sel_branches))})"
        params.extend(sel_branches)

    df_explore = pd.read_sql(base_query, conn, params=params or None)

    # Checkbox - black text
    fraud_only = st.checkbox("🔴 Show only fraud cases", value=False)
    if fraud_only:
        df_explore = df_explore[df_explore['status'] == 'Fraud']

    st.markdown(f"**Showing {len(df_explore):,} transactions**")
    st.dataframe(df_explore.head(1000), use_container_width=True)

# === Real-Time Fraud Predictor ===
elif page == "Real-Time Fraud Predictor":
    st.markdown("<h2 style='color:#002D72; text-align:center;'>🤖 Real-Time Fraud Risk Prediction</h2>", unsafe_allow_html=True)

    with st.form("predict_form", clear_on_submit=False):
        st.markdown("**Enter transaction details below:**")
        col1, col2 = st.columns(2)
        amount = col1.number_input("Amount (ETB)", min_value=50.0, value=15000.0, step=500.0)
        channel = col2.selectbox("Channel", transaction_channels)

        location = st.selectbox("Transaction Location (Branch)", branches)
        home_branch = st.selectbox("Customer Home Branch", branches)
        hour = st.slider("Hour of Day (0-23)", 0, 23, 12)
        balance = st.number_input("Customer Balance (ETB)", min_value=0.0, value=50000.0)

        submitted = st.form_submit_button("🔍 Predict Fraud Risk", use_container_width=True)

    if submitted:
        location_mismatch = 1 if location != home_branch else 0
        high_amount = 1 if amount > 15000 else 0
        is_weekend = 0

        input_df = pd.DataFrame([{
            'amount_etb': amount,
            'hour': hour,
            'is_weekend': is_weekend,
            'location_mismatch': location_mismatch,
            'high_amount': high_amount,
            'balance_etb': balance
        }])

        for ch in transaction_channels:
            input_df[f'channel_{ch}'] = 1 if channel == ch else 0

        input_df = input_df.reindex(columns=expected_features, fill_value=0)

        prob = model.predict_proba(input_df)[0][1]
        pred = model.predict(input_df)[0]

        if pred == 1 or prob > 0.5:
            st.error(f"🚨 **HIGH FRAUD RISK** – Probability: {prob*100:.1f}%")
            st.warning("Recommended: Flag for review / Block transaction")
        else:
            st.success(f"✅ **Low Risk** – Probability: {prob*100:.1f}%")
            st.balloons()

        st.markdown(f"<p style='color:#333333; font-weight:bold; font-size:18px;'>Key factors: {'Location Mismatch' if location_mismatch else 'Normal location'} | "
                    f"Amount {'High (>15k ETB)' if high_amount else 'Normal'} | Channel: {channel}</p>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'><strong>Developed by Aklilu Abera</strong> • Portfolio Project for Data Analyst & BI Developer Role • December 2025</div>", unsafe_allow_html=True)

