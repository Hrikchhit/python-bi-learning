# Lesson 1 — pandas Deep Dive

## groupby
```python
completed = df[df['status'] == 'completed']

summary = completed.groupby('city').agg(
    total_revenue = ('amount', 'sum'),
    total_orders  = ('order_id', 'count'),
    avg_order     = ('amount', 'mean')
).reset_index()
```

## merge
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

## apply — single column
```python
def label(value):
    if value >= 1000:
        return 'High'
    elif value >= 100:
        return 'Medium'
    else:
        return 'Low'

df['size'] = df['amount'].apply(label)
```

## apply — multiple columns (axis=1)
```python
def label(row):               # name it 'row' not 'df'
    if row['city'] == 'Melbourne' and row['amount'] > 500:
        return 'High value major'
    return 'Other'

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
- Filter BEFORE groupby — better performance
- reset_index() after groupby — proper column names
- .copy() when passing to functions — protect original
- [] for selecting, () for calling
- enumerate() for chart labels — always correct position
