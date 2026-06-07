# ============================================
# Lesson 4: ETL Pipeline — Practice Problems
# Environment: Google Colab
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

sales_data = pd.DataFrame({
    'order_id':   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'customer':   ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob',
                   'Diana', 'Charlie', 'Eve', 'Diana', 'Eve'],
    'product':    ['Laptop', 'Mouse', 'Laptop', 'Keyboard', 'Mouse',
                   'Laptop', 'Mouse', 'Monitor', 'Laptop', 'Laptop'],
    'category':   ['Electronics', 'Accessories', 'Electronics', 'Accessories',
                   'Accessories', 'Electronics', 'Accessories', 'Electronics',
                   'Electronics', 'Electronics'],
    'amount':     [1200, 25, 1200, 45, 25, 1200, 25, 350, 1200, 1200],
    'status':     ['completed', 'completed', 'completed', 'cancelled',
                   'completed', 'completed', 'completed', 'completed',
                   'completed', 'completed'],
    'order_date': pd.date_range(start='2024-01-01', periods=10, freq='ME'),
    'city':       ['Melbourne', 'Sydney', 'Melbourne', 'Brisbane', 'Sydney',
                   'Melbourne', 'Brisbane', 'Sydney', 'Melbourne', 'Sydney']
})


# -----------------------------------------------
# FULL ETL PIPELINE
# -----------------------------------------------
def extract(data):
    print("Step 1: Data extracted")
    print(f"   Shape: {data.shape}")
    return data.copy()

def transform(df):
    df = df[df['status'] == 'completed'].copy()
    df['month'] = df['order_date'].dt.strftime('%Y-%m')

    def label_size(amount):
        if amount >= 1000:
            return 'High'
        elif amount >= 100:
            return 'Medium'
        else:
            return 'Low'

    df['order_size'] = df['amount'].apply(label_size)
    print("Step 2: Data transformed")
    print(f"   Completed orders: {len(df)}")
    return df

def analyse(df):
    city_summary = df.groupby('city').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count'),
        avg_order     = ('amount', 'mean')
    ).reset_index().sort_values('total_revenue', ascending=False)
    city_summary['avg_order'] = city_summary['avg_order'].round(2)

    product_summary = df.groupby('product').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index().sort_values('total_revenue', ascending=False)

    month_summary = df.groupby('month').agg(
        total_revenue = ('amount', 'sum'),
        total_orders  = ('order_id', 'count')
    ).reset_index()

    print("Step 3: Analysis complete")
    print(f"   Cities: {len(city_summary)}")
    print(f"   Products: {len(product_summary)}")
    print(f"   Months: {len(month_summary)}")
    return city_summary, product_summary, month_summary

def export(city, product, month, clean):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename  = f'sales_report_{timestamp}.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        city.to_excel(writer,    sheet_name='By City',    index=False)
        product.to_excel(writer, sheet_name='By Product', index=False)
        month.to_excel(writer,   sheet_name='Monthly',    index=False)
        clean.to_excel(writer,   sheet_name='Raw Data',   index=False)
    print(f"Step 4: Exported → {filename}")
    return filename

def run_pipeline(data):
    print("Starting pipeline...")
    print("-" * 40)
    raw                      = extract(data)
    clean                    = transform(raw)
    city, product, month     = analyse(clean)
    filename                 = export(city, product, month, clean)
    print("-" * 40)
    print(f"Pipeline complete! → {filename}")
    return city, product, month, clean

city_summary, product_summary, month_summary, clean_data = run_pipeline(sales_data)

print("\nCity Summary:")
print(city_summary)
print("\nProduct Summary:")
print(product_summary)
