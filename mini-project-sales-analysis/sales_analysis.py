# ============================================
# Phase 2 Mini Project — Sales Analysis Report
# Author: Hrikchhit
# Tool: Google Colab / Python 3.12
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re

# -----------------------------------------------
# RAW DATA
# -----------------------------------------------
raw_data = pd.DataFrame({
    'order_id':   [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    'customer':   ['ALICE','bob','Alice','CHARLIE','bob','Diana','CHARLIE',
                   'eve','Diana','EVE','alice','BOB','Charlie','DIANA','Eve',
                   'Alice','BOB','charlie','Diana','eve'],
    'product':    ['Laptop','Mouse','Laptop','Keyboard','Monitor','Laptop',
                   'Mouse','Monitor','Laptop','Keyboard','Mouse','Laptop',
                   'Monitor','Keyboard','Laptop','Mouse','Laptop','Keyboard',
                   None,'Monitor'],
    'category':   ['Electronics','Accessories','Electronics','Accessories',
                   'Electronics','Electronics','Accessories','Electronics',
                   'Electronics','Accessories','Accessories','Electronics',
                   'Electronics','Accessories','Electronics','Accessories',
                   'Electronics','Accessories','Electronics','Electronics'],
    'amount':     [1200,25,1200,45,350,1200,25,350,1200,45,25,1200,
                   350,'45',1200,25,1200,45,None,350],
    'status':     ['completed','completed','completed','cancelled','completed',
                   'completed','completed','COMPLETED','completed','completed',
                   'completed','cancelled','completed','completed','COMPLETED',
                   'completed','completed','cancelled','completed','completed'],
    'order_date': ['2024-01-05','2024-01-20','2024-02-10','2024-01-15',
                   '2024-02-28','2024-03-01','2024-03-10','03/22/2024',
                   '2024-04-05','2024-04-18','2024-05-02','2024-05-15',
                   '2024-06-01','2024-06-20','07/15/2024','2024-07-28',
                   '2024-08-10','2024-08-22','invalid','2024-09-05'],
    'city':       ['Melbourne','Sydney','Melbourne ','Brisbane','Sydney',
                   ' Melbourne','Brisbane','Sydney','Melbourne','Sydney',
                   'Melbourne','Sydney','Brisbane',' Melbourne','Sydney',
                   'Melbourne','Sydney','Brisbane','Melbourne','Sydney'],
    'segment':    ['Premium','Standard','Premium','Standard','Standard',
                   'Premium','Standard','Standard','Premium','Standard',
                   'Premium','Standard','Standard','Premium','Standard',
                   'Premium','Standard','Standard','Premium','Standard']
})


# -----------------------------------------------
# STEP 1 — CLEAN
# -----------------------------------------------
def clean(df):
    df = df.copy()
    df['customer']   = df['customer'].str.title()
    df['city']       = df['city'].str.strip()
    df['status']     = df['status'].str.lower()
    df['amount']     = pd.to_numeric(df['amount'], errors='coerce')
    df['order_date'] = df['order_date'].str.replace(
        r'(\d{2})/(\d{2})/(\d{4})', r'\3-\1-\2', regex=True)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['product', 'amount', 'order_date'])
    return df


# -----------------------------------------------
# STEP 2 — TRANSFORM
# -----------------------------------------------
def transform(df):
    df = df.copy()
    df['month'] = df['order_date'].dt.strftime('%Y-%m')

    def label_size(amount):
        if amount >= 1000:
            return 'High'
        elif amount >= 100:
            return 'Medium'
        else:
            return 'Low'

    df['order_size'] = df['amount'].apply(label_size)
    return df


# -----------------------------------------------
# STEP 3 — ANALYSE
# -----------------------------------------------
def analyse(df):
    completed = df[df['status'] == 'completed']

    city_summary = completed.groupby('city').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index().sort_values('total_revenue', ascending=False)

    product_summary = completed.groupby('product').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index().sort_values('total_revenue', ascending=False)

    monthly_summary = completed.groupby('month').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index()

    segment_summary = completed.groupby('segment').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index().sort_values('total_revenue', ascending=False)

    return city_summary, product_summary, monthly_summary, segment_summary


# -----------------------------------------------
# STEP 4 — VISUALISE
# -----------------------------------------------
def visualise(city, product, monthly, segment):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Sales Performance Report — 2024',
                 fontsize=16, fontweight='bold')

    sns.barplot(data=city, x='city', y='total_revenue',
                hue='city', palette='Blues_d', legend=False, ax=axes[0,0])
    axes[0,0].set_title('Revenue by City')
    axes[0,0].set_xlabel('City')
    axes[0,0].set_ylabel('Revenue ($)')
    for i, val in enumerate(city['total_revenue']):
        axes[0,0].text(i, val + 20, f'${val:,.0f}', ha='center', fontsize=9)

    sns.barplot(data=product, x='product', y='total_revenue',
                hue='product', palette='Greens_d', legend=False, ax=axes[0,1])
    axes[0,1].set_title('Revenue by Product')
    axes[0,1].set_xlabel('Product')
    axes[0,1].set_ylabel('Revenue ($)')
    for i, val in enumerate(product['total_revenue']):
        axes[0,1].text(i, val + 20, f'${val:,.0f}', ha='center', fontsize=9)

    monthly_sorted = monthly.sort_values('month')
    axes[1,0].plot(monthly_sorted['month'], monthly_sorted['total_revenue'],
                   marker='o', linewidth=2, color='steelblue')
    axes[1,0].set_title('Monthly Revenue Trend')
    axes[1,0].set_xlabel('Month')
    axes[1,0].set_ylabel('Revenue ($)')
    axes[1,0].tick_params(axis='x', rotation=45)

    sns.barplot(data=segment, x='segment', y='total_revenue',
                hue='segment', palette='Oranges_d', legend=False, ax=axes[1,1])
    axes[1,1].set_title('Revenue by Customer Segment')
    axes[1,1].set_xlabel('Segment')
    axes[1,1].set_ylabel('Revenue ($)')
    for i, val in enumerate(segment['total_revenue']):
        axes[1,1].text(i, val + 20, f'${val:,.0f}', ha='center', fontsize=9)

    plt.tight_layout()
    plt.show()


# -----------------------------------------------
# STEP 5 — EXPORT
# -----------------------------------------------
def export(city, product, monthly, segment, clean):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename  = f'sales_report_{timestamp}.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        city.to_excel(writer,    sheet_name='By City',    index=False)
        product.to_excel(writer, sheet_name='By Product', index=False)
        monthly.to_excel(writer, sheet_name='Monthly',    index=False)
        segment.to_excel(writer, sheet_name='By Segment', index=False)
        clean.to_excel(writer,   sheet_name='Clean Data', index=False)
    print(f"✅ File exported: {filename}")
    return filename


# -----------------------------------------------
# MASTER PIPELINE
# -----------------------------------------------
def run(data):
    print("🚀 Starting Sales Analysis Pipeline...")
    print("-" * 45)

    clean_df        = clean(data)
    print(f"✅ Step 1: Cleaned — {clean_df.shape[0]} rows")

    transformed     = transform(clean_df)
    print(f"✅ Step 2: Transformed — added month + order_size")

    city, product, monthly, segment = analyse(transformed)
    print(f"✅ Step 3: Analysed — {len(city)} cities, {len(product)} products")

    visualise(city, product, monthly, segment)
    print(f"✅ Step 4: Charts generated")

    filename = export(city, product, monthly, segment, transformed)
    print(f"✅ Step 5: Exported → {filename}")

    print("-" * 45)
    print("🎉 Pipeline complete!")
    return city, product, monthly, segment, transformed

# Run!
city_summary, product_summary, monthly_summary, segment_summary, final_data = run(raw_data)
