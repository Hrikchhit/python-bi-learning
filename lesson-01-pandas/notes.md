# Lesson 1 — pandas Deep Dive

## groupby
```python
# Filter first, then groupby
completed = df[df['status'] == 'completed']

summary = completed.groupby('city').agg(
    total_revenue = ('amount', 'sum'),
    total_orders  = ('order_id', 'count'),
    avg_order     = ('amount', 'mean')
).reset_index()  # always reset_index after groupby
```

## merge (SQL JOINs in pandas)
```python
merged = df1.merge(df2, on='customer_id', how='left')
# how= 'inner', 'left', 'right', 'outer'
```

## pivot_table
```python
pivot = df.pivot_table(
    values     = 'amount',
    index      = 'product',
    columns    = 'month',
    aggfunc    = 'sum',
    fill_value = 0
)
```

## apply
```python
# Single column
def label(value):
    if value >= 1000:
        return 'High'
    return 'Low'
df['size'] = df['amount'].apply(label)

# Multiple columns (axis=1)
def label(row):
    if row['city'] == 'Melbourne' and row['amount'] > 500:
        return 'High value major'
df['col'] = df.apply(label, axis=1)
```

## Top N per group pattern
```python
top = (df
    .groupby(['city', 'product'])['order_id']
    .count()
    .reset_index()
    .sort_values('order_id', ascending=False)
    .groupby('city')['product']
    .first()
    .reset_index()
)
```

## Key rules
- Filter BEFORE groupby
- reset_index() after groupby
- .copy() when passing to functions
- [] for selecting, () for calling
- Series vs DataFrame — reset_index() gives proper column names
