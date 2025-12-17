#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Awash Bank Fraud Analytics", layout="wide")

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

# PROFESSIONAL & HIGH-VISIBILITY CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
        background-image: none;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #002D72 !important;
        font-weight: bold;
    }
    .stMarkdown p, .stMarkdown div, .stText, .stCaption {
        color: #333333 !important;
        font-size: 16px !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #002D72 !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    label {
        color: black !important;
        font-weight: bold !important;
        font-size: 17px !important;
    }
    .stCheckbox label {
        color: black !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 6px solid #002D72;
    }
    .stButton > button {
        background-color: #002D72;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #333333 !important;
    }
    div[data-testid="stDataFrame"] {
        background-color: white !important;
    }
    .stMetric > label, .stMetric > div[data-testid="stMetricValue"] {
        color: #333333 !important;
    }
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

# Load Model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('fraud_model.pkl')
        features = joblib.load('model_features.pkl')
        return model, features
    except Exception as e:
        st.error(f"Model load failed: {e}")
        st.stop()

model, expected_features = load_model()

# Load data from your CSV files
@st.cache_data
def load_data():
    try:
        # Your exact CSV filenames
        transactions = pd.read_csv('awash_transactions.csv')
        customers = pd.read_csv('awash_customers.csv')
        
        # Merge on account_number
        df = transactions.merge(customers, on='account_number', how='left')
        return df
    except FileNotFoundError as e:
        st.error(f"CSV file not found: {e}. Please ensure 'awash_transaction.csv' and 'awash_customer.csv' are in the repository root.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()

# Header
st.markdown("<div style='text-align: center; margin-bottom: 40px;'>", unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Awash_Bank_Final_logo.jpg/800px-Awash_Bank_Final_logo.jpg", width=220)
st.markdown("<h1 style='color:#002D72;'>🏦 Awash Bank Fraud Detection & Risk Analytics Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color:#555;'>Real-time monitoring and predictive fraud detection system simulating Awash Bank S.C. operations in Ethiopia</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h3 style='color:white; text-align:center;'>Navigation</h3>", unsafe_allow_html=True)
page = st.sidebar.radio("Select Page", ["Overview Dashboard", "Fraud Explorer", "Real-Time Fraud Predictor"], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:white; text-align:center;'>Developed by Aklilu Abera</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:white; text-align:center; font-size:14px;'>Portfolio Project • December 2025</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:white; text-align:center; font-size:14px;'>Built with Python, scikit-learn & Streamlit</p>", unsafe_allow_html=True)

# === Overview Dashboard ===
if page == "Overview Dashboard":
    st.markdown("<h2 style='color:#002D72; text-align:center;'>🔍 Key Metrics & Insights</h2>", unsafe_allow_html=True)

    total_transactions = len(df)
    total_fraud = df['fraud_flag'].sum()
    avg_amount = df['amount_etb'].mean()
    fraud_amount_etb = df[df['fraud_flag'] == 1]['amount_etb'].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Transactions", f"{total_transactions:,}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Fraud Cases Detected", f"{total_fraud:,}", delta=f"{(total_fraud/total_transactions)*100:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Average Amount (ETB)", f"{avg_amount:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Fraud Amount at Risk (ETB)", f"{fraud_amount_etb:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<h3 style='color:#002D72;'>Fraud Rate by Channel</h3>", unsafe_allow_html=True)
        channel_df = df.groupby('channel')['fraud_flag'].mean().reset_index()
        channel_df['fraud_rate'] = channel_df['fraud_flag'] * 100
        channel_df = channel_df.sort_values('fraud_rate', ascending=False)

        fig, ax = plt.subplots(figsize=(11,6))
        sns.barplot(data=channel_df, x='channel', y='fraud_rate', palette='Blues_d', ax=ax)
        ax.set_title("Fraud Rate by Channel (%)", fontsize=14)
        ax.set_ylabel("Fraud Rate (%)")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with col_right:
        st.markdown("<h3 style='color:#002D72;'>Top 15 Branches by Fraud Rate</h3>", unsafe_allow_html=True)
        branch_df = df.groupby('home_branch')['fraud_flag'].mean().reset_index()
        branch_df['fraud_rate'] = branch_df['fraud_flag'] * 100
        branch_df = branch_df.sort_values('fraud_rate', ascending=False).head(15)

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

    df_explore = df.copy()

    if sel_channels:
        df_explore = df_explore[df_explore['channel'].isin(sel_channels)]
    if sel_branches:
        df_explore = df_explore[df_explore['home_branch'].isin(sel_branches)]

    df_explore['status'] = df_explore['fraud_flag'].apply(lambda x: 'Fraud' if x == 1 else 'Normal')

    fraud_only = st.checkbox("🔴 Show only fraud cases", value=False)
    if fraud_only:
        df_explore = df_explore[df_explore['status'] == 'Fraud']

    st.markdown(f"**Showing {len(df_explore):,} transactions**")
    display_cols = ['transaction_id', 'date', 'amount_etb', 'channel', 'location', 'merchant', 'status', 'home_branch', 'balance_etb']
    st.dataframe(df_explore[display_cols].head(1000), use_container_width=True)

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

        # Black text for prediction results
        if pred == 1 or prob > 0.5:
            st.markdown(f"<p style='color:black; font-size:20px; font-weight:bold;'>🚨 **HIGH FRAUD RISK** – Probability: {prob*100:.1f}%</p>", unsafe_allow_html=True)
            st.markdown("<p style='color:black; font-size:18px; font-weight:bold;'>Recommended: Flag for review / Block transaction</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:black; font-size:20px; font-weight:bold;'>✅ **Low Risk** – Probability: {prob*100:.1f}%</p>", unsafe_allow_html=True)
            st.balloons()

        st.markdown(f"<p style='color:black; font-weight:bold; font-size:18px;'>Key factors: {'Location Mismatch' if location_mismatch else 'Normal location'} | "
                    f"Amount {'High (>15k ETB)' if high_amount else 'Normal'} | Channel: {channel}</p>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'><strong>Developed by Aklilu Abera</strong> • Portfolio Project for Data Analyst & BI Developer Role • December 2025</div>", unsafe_allow_html=True)


# In[ ]:




