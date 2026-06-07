# ============================================
# Lesson 3: Visualisation — Practice Problems
# Environment: Google Colab
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# CHART 1: Bar chart — revenue by city
# -----------------------------------------------
city_revenue = (
    sales_data[sales_data['status'] == 'completed']
    .groupby('city')['amount'].sum()
    .reset_index()
    .sort_values('amount', ascending=False)
    .reset_index(drop=True)
)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=city_revenue, x='city', y='amount',
    hue='city', palette='Blues_d', legend=False
)
plt.title('Total Revenue by City', fontsize=14, fontweight='bold')
plt.xlabel('City')
plt.ylabel('Total Revenue ($)')
for i, amount in enumerate(city_revenue['amount']):
    plt.text(i, amount + 20, f"${amount:,.0f}", ha='center', fontsize=10)
plt.tight_layout()
plt.show()


# -----------------------------------------------
# CHART 2: Line chart — monthly trend
# -----------------------------------------------
monthly_revenue = (
    sales_data[sales_data['status'] == 'completed']
    .groupby(sales_data['order_date'].dt.strftime('%Y-%m'))['amount']
    .sum()
    .reset_index()
)
monthly_revenue.columns = ['month', 'amount']

plt.figure(figsize=(12, 5))
plt.plot(monthly_revenue['month'], monthly_revenue['amount'],
         marker='o', linewidth=2, color='steelblue')
plt.title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -----------------------------------------------
# CHART 3: Heatmap — revenue by product and month
# -----------------------------------------------
heatmap_data = (
    sales_data[sales_data['status'] == 'completed']
    .groupby([
        sales_data['order_date'].dt.strftime('%Y-%m'),
        'product'
    ])['amount']
    .sum()
    .unstack(fill_value=0)
)

plt.figure(figsize=(12, 5))
sns.heatmap(heatmap_data, annot=True, fmt=',.0f',
            cmap='Blues', linewidths=0.5)
plt.title('Revenue by Product and Month', fontsize=14, fontweight='bold')
plt.xlabel('Product')
plt.ylabel('Month')
plt.tight_layout()
plt.show()


# -----------------------------------------------
# MINI CHALLENGE: bar chart — revenue by product
# -----------------------------------------------
product_revenue = (
    sales_data[sales_data['status'] == 'completed']
    .groupby('product')['amount'].sum()
    .reset_index()
    .sort_values('amount', ascending=False)
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=product_revenue, x='product', y='amount',
    hue='product', palette='Blues_d', legend=False
)
plt.title('Total Revenue by Product', fontsize=14, fontweight='bold')
plt.xlabel('Product')
plt.ylabel('Total Revenue ($)')
for i, amount in enumerate(product_revenue['amount']):
    plt.text(i, amount + 20, f"${amount:,.0f}", ha='center', fontsize=10)
plt.tight_layout()
plt.show()
