#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import random
from datetime import datetime, timedelta
import os

# ----------------------------- CONFIG -----------------------------
NUM_CUSTOMERS = 10000
NUM_TRANSACTIONS = 100000
DATA_DIR = "../data"
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------------- REALISTIC LISTS -------------------------
# Common Ethiopian first and last names (curated for realism)
first_names = [
    "Abebe", "Tsehay", "Yohannes", "Selamawit", "Dawit", "Genet", "Mulugeta", "Aster",
    "Birhanu", "Fatuma", "Kebede", "Meseret", "Tesfaye", "Zewdu", "Hiwot", "Lemma",
    "Workneh", "Eyerusalem", "Getachew", "Almaz", "Mohammed", "Fitsum", "Rahel", "Tadesse"
]

last_names = [
    "Kebede", "Alemu", "Tadesse", "Assefa", "Worku", "Mengistu", "Girma", "Demissie",
    "Bekele", "Teshome", "Abebe", "Mulugeta", "Shiferaw", "Gebre", "Hailu", "Kassahun",
    "Yilma", "Negussie", "Solomon", "Berhanu", "Desta", "Wondimu", "Lemma", "Fantahun"
]

# Real/semi-real Awash Bank branch names (based on public info)
branches = [
    "Awash Towers Headquarters - Addis Ababa",
    "Bole Branch - Addis Ababa",
    "Kirkos Branch - Addis Ababa",
    "Mexico Square Branch - Addis Ababa",
    "Piassa Branch - Addis Ababa",
    "Merkato Branch - Addis Ababa",
    "Dire Dawa Branch",
    "Bahir Dar Branch",
    "Mekelle Branch",
    "Jimma Branch",
    "Awassa Branch",
    "Adama Branch",
    "Gondar Branch",
    "Dessie Branch",
    "Harar Branch",
    "Shashemene Branch",
    "Arba Minch Branch",
    "Debre Birhan Branch"
]

account_types = [
    "Savings Account",
    "Current Account",
    "Wadiah Saving (Interest-Free)",
    "Diaspora Foreign Currency",
    "Lucy Women Saving"
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

# ------------------------- GENERATE CUSTOMERS -------------------------
print("Generating customers...")
customers = []
for i in range(NUM_CUSTOMERS):
    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"
    
    # Ethiopian phone: +251-9 followed by 8 digits
    phone = f"+251-9{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}-{random.randint(0,999999):06d}"
    
    # 13-digit account number (common in Ethiopian banks)
    account_number = random.randint(10**12, 10**13 - 1)
    
    customers.append({
        "customer_id": 100000 + i,
        "full_name": full_name,
        "phone": phone,
        "address": f"{random.choice(['Bole', 'Kirkos', 'Piassa', 'Merkato', 'Lideta', 'Yeka', 'Addis Ketema'])} Sub-City, Addis Ababa" 
                   if random.random() < 0.6 else f"{random.choice(['Dire Dawa', 'Bahir Dar', 'Mekelle', 'Jimma'])}",
        "account_number": account_number,
        "account_type": random.choice(account_types),
        "balance_etb": round(random.uniform(500, 500000), 2),
        "home_branch": random.choice(branches),
        "join_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d")
    })

df_customers = pd.DataFrame(customers)
customer_path = os.path.join(DATA_DIR, "awash_customers.csv")
df_customers.to_csv(customer_path, index=False)
print(f"Customers saved to {customer_path} ({len(df_customers)} rows)")

# ----------------------- GENERATE TRANSACTIONS -----------------------
print("Generating transactions...")
transactions = []
fraud_count = 0

for _ in range(NUM_TRANSACTIONS):
    customer = random.choice(customers)
    amount = round(random.uniform(50, 60000), 2)
    channel = random.choice(transaction_channels)
    
    # Determine location (usually home branch, sometimes different)
    location_mismatch = random.random() < 0.15  # 15% chance of different location
    location = random.choice(branches) if location_mismatch else customer["home_branch"]
    
    # Simple fraud rules (realistic patterns)
    is_fraud = 0
    if (amount > 15000 and location_mismatch) or \
       (amount > 30000 and channel == "AwashBirr Mobile Transfer") or \
       (random.random() < 0.005):  # Rare random fraud
        is_fraud = 1
        fraud_count += 1
    
    transactions.append({
        "transaction_id": 1000000 + _,
        "account_number": customer["account_number"],
        "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S"),
        "amount_etb": amount,
        "channel": channel,
        "location": location,
        "merchant": random.choice(["Ethio Telecom", "Local Shop", "Supermarket", "Fuel Station", "Internal Transfer", "Utility Bill"]) 
                    if channel in ["POS Payment", "Bill Payment"] else "N/A",
        "fraud_flag": is_fraud
    })

df_transactions = pd.DataFrame(transactions)
transaction_path = os.path.join(DATA_DIR, "awash_transactions.csv")
df_transactions.to_csv(transaction_path, index=False)
print(f"Transactions saved to {transaction_path} ({len(df_transactions)} rows)")
print(f"Fraud rate: {fraud_count / len(df_transactions) * 100:.2f}% ({fraud_count} fraudulent transactions)")


# In[ ]:




