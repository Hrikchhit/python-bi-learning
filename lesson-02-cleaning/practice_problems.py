# ============================================
# Lesson 2: Data Cleaning — Practice Problems
# Environment: Google Colab
# ============================================

import pandas as pd
import numpy as np


# -----------------------------------------------
# PROBLEM 1: Full cleaning pipeline
# -----------------------------------------------
messy_data = pd.DataFrame({
    'order_id':   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'customer':   ['Alice', 'BOB', 'alice', 'Charlie', 'bob',
                   'Diana', 'CHARLIE', 'Eve', 'Diana', None, 'Eve'],
    'product':    ['Laptop', 'Mouse', 'Laptop', 'Keyboard', 'Mouse',
                   'Laptop', 'Keyboard', 'Monitor', 'Laptop', 'Mouse', None],
    'amount':     [1200, 25, 1200, 45, 25, 1200, '45', 350, 1200, None, 350],
    'order_date': ['2024-01-05', '2024-01-20', '2024-02-10', '2024-01-15',
                   '2024-02-28', '2024-03-01', '2024-03-10', '2024-03-22',
                   '05/04/2024', 'invalid_date', '2024-04-18'],
    'city':       ['Melbourne', 'Sydney', 'Melbourne ', ' Sydney', 'Sydney',
                   'Brisbane', 'Melbourne', 'Sydney', 'Brisbane', 'Sydney', 'Sydney'],
    'status':     ['completed', 'completed', 'completed', 'cancelled', 'completed',
                   'completed', 'COMPLETED', 'completed', 'completed', 'completed', 'completed']
})

def clean_sales_data(df):
    df = df.copy()
    df['customer']   = df['customer'].str.title()
    df['status']     = df['status'].str.lower()
    df['city']       = df['city'].str.strip()
    df['amount']     = pd.to_numeric(df['amount'], errors='coerce')
    df['order_date'] = df['order_date'].str.replace(
        r'(\d{2})/(\d{2})/(\d{4})', r'\3-\2-\1', regex=True
    )
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['customer', 'product', 'amount', 'order_date'])
    df = df.drop_duplicates()
    return df

clean_df = clean_sales_data(messy_data.copy())
print("Problem 1 — Cleaned Data:")
print(clean_df)


# -----------------------------------------------
# PROBLEM 2: CRM data cleaning + city summary
# -----------------------------------------------
crm_data = pd.DataFrame({
    'order_id':  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'customer':  ['JOHN', 'jane', 'John', 'MIKE', 'jane',
                  'Sarah', 'mike', None, 'Sarah', 'John'],
    'city':      ['Melbourne ', ' Sydney', 'Melbourne', 'Brisbane', 'Sydney',
                  ' Melbourne', 'Brisbane', 'Sydney', 'Melbourne', 'Sydney'],
    'amount':    [500, 300, 500, '250', 150, 800, 250, 300, '800', None],
    'order_date':['2024-01-10', '2024-01-15', '01/02/2024', '2024-02-20',
                  '2024-03-05', '2024-03-15', '2024-04-01', 'invalid',
                  '2024-04-10', '2024-04-20'],
    'status':    ['completed', 'COMPLETED', 'completed', 'cancelled', 'completed',
                  'completed', 'COMPLETED', 'completed', 'completed', 'completed']
})

def clean_crm(df):
    df = df.copy()
    df['customer']   = df['customer'].str.title()
    df['status']     = df['status'].str.lower()
    df['city']       = df['city'].str.strip()
    df['amount']     = pd.to_numeric(df['amount'], errors='coerce')
    df['order_date'] = df['order_date'].str.replace(
        r'(\d{2})/(\d{2})/(\d{4})', r'\3-\2-\1', regex=True
    )
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['customer', 'amount', 'order_date'])
    df = df.drop_duplicates()
    return df

crm_cleaned = clean_crm(crm_data.copy())
city_summary = (crm_cleaned[crm_cleaned['status'] == 'completed']
    .groupby('city').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index()
)

print("\nProblem 2 — CRM City Summary:")
print(city_summary)
