# Lesson 3 — matplotlib & seaborn

## Bar chart
```python
plt.figure(figsize=(8, 5))
sns.barplot(
    data=df, x='city', y='amount',
    hue='city', palette='Blues_d', legend=False
)
plt.title('Title', fontsize=14, fontweight='bold')
plt.xlabel('X Label')
plt.ylabel('Y Label')
for i, amount in enumerate(df['amount']):
    plt.text(i, amount + 20, f"${amount:,.0f}", ha='center')
plt.tight_layout()
plt.show()
```

## Line chart
```python
plt.figure(figsize=(12, 5))
sns.lineplot(data=df, x='month', y='amount', marker='o')
plt.title('Monthly Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Heatmap
```python
heatmap_data = df.groupby(['month', 'product'])['amount']\
    .sum().unstack(fill_value=0)

plt.figure(figsize=(12, 5))
sns.heatmap(heatmap_data, annot=True, fmt=',.0f',
            cmap='Blues', linewidths=0.5)
plt.tight_layout()
plt.show()
```

## Key concepts
- figsize=(w, h) — canvas size in inches
- marker='o' — dot at each data point
- rotation=45 — rotate x labels
- annot=True — show values in heatmap cells
- cmap='Blues' — colour scheme
- unstack() — pivot multi-index to columns
- tight_layout() — always before show()
- enumerate() — loop with position (0,1,2...)
- hue + legend=False — fixes FutureWarning in seaborn

## When to use which chart
- Bar chart — comparing categories
- Line chart — trends over time
- Heatmap — matrix of two dimensions
