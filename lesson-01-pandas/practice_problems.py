# ============================================
# Lesson 1: pandas Deep Dive — Practice Problems
# Environment: Google Colab
# ============================================

import pandas as pd
import numpy as np

# Dataset
orders = pd.DataFrame({
    'order_id':    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'customer_id': [101, 101, 102, 103, 102, 104, 103, 101, 104, 105],
    'product':     ['Laptop', 'Mouse', 'Laptop', 'Keyboard', 'Monitor',
                    'Laptop', 'Mouse', 'Monitor', 'Keyboard', 'Laptop'],
    'category':    ['Electronics', 'Accessories', 'Electronics', 'Accessories',
                    'Electronics', 'Electronics', 'Accessories', 'Electronics',
                    'Accessories', 'Electronics'],
    'amount':      [1200, 25, 1200, 45, 350, 1200, 25, 350, 45, 1200],
    'status':      ['completed', 'completed', 'completed', 'cancelled',
                    'completed', 'completed', 'completed', 'cancelled',
                    'completed', 'completed'],
    'order_date':  ['2024-01-05', '2024-01-20', '2024-02-10', '2024-01-15',
                    '2024-02-28', '2024-03-01', '2024-03-10', '2024-03-22',
                    '2024-04-05', '2024-04-18']
})

customers = pd.DataFrame({
    'customer_id': [101, 102, 103, 104, 105],
    'name':        ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'city':        ['Melbourne', 'Sydney', 'Melbourne', 'Brisbane', 'Sydney'],
    'segment':     ['Premium', 'Standard', 'Standard', 'Premium', 'Standard']
})

orders['order_date'] = pd.to_datetime(orders['order_date'])


# -----------------------------------------------
# PROBLEM 1: groupby — customer summary
# -----------------------------------------------
completed = orders[orders['status'] == 'completed']

customer_summary = completed.groupby('customer_id').agg(
    total_orders    = ('order_id', 'count'),
    total_revenue   = ('amount', 'sum'),
    avg_order_value = ('amount', 'mean')
).reset_index()

print("Problem 1 — Customer Summary:")
print(customer_summary)


# -----------------------------------------------
# PROBLEM 2: merge — enrich with customer info
# -----------------------------------------------
enriched_summary = customer_summary.merge(
    customers, on='customer_id', how='left'
)

print("\nProblem 2 — Enriched Summary:")
print(enriched_summary)


# -----------------------------------------------
# PROBLEM 3: pivot_table — revenue by product and month
# -----------------------------------------------
orders['month'] = orders['order_date'].dt.to_period('M')

product_pivot = orders[orders['status'] == 'completed'].pivot_table(
    values     = 'amount',
    index      = 'product',
    columns    = 'month',
    aggfunc    = 'sum',
    fill_value = 0
)

print("\nProblem 3 — Product Pivot:")
print(product_pivot)


# -----------------------------------------------
# PROBLEM 4: apply — customer tier
# -----------------------------------------------
def tier_order(total_revenue):
    if total_revenue >= 1500:
        return 'Platinum'
    elif total_revenue >= 500:
        return 'Gold'
    else:
        return 'Silver'

enriched_summary['customer_tier'] = enriched_summary['total_revenue'].apply(tier_order)

print("\nProblem 4 — Customer Tiers:")
print(enriched_summary[['customer_id', 'name', 'total_revenue', 'customer_tier']])


# -----------------------------------------------
# MINI CHALLENGE: city performance report
# -----------------------------------------------
merged_data = orders.merge(customers, on='customer_id', how='left')
completed   = merged_data[merged_data['status'] == 'completed']

city_summary = completed.groupby('city').agg(
    total_revenue   = ('amount', 'sum'),
    total_orders    = ('order_id', 'count'),
    avg_order_value = ('amount', 'mean')
).reset_index()
city_summary['avg_order_value'] = city_summary['avg_order_value'].round(2)

top_products = (
    completed
    .groupby(['city', 'product'])['order_id']
    .count()
    .reset_index()
    .sort_values('order_id', ascending=False)
    .groupby('city')['product']
    .first()
    .reset_index()
    .rename(columns={'product': 'top_product'})
)

final_report = city_summary.merge(top_products, on='city', how='left')
print("\nMini Challenge — City Report:")
print(final_report)
