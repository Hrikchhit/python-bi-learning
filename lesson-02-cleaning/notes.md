# Lesson 2 — Data Cleaning

## Full cleaning pipeline
```python
def clean_data(df):
    df = df.copy()                # protect original
    df['customer'] = df['customer'].str.title()
    df['status']   = df['status'].str.lower()
    df['city']     = df['city'].str.strip().str.title()
    df['amount']   = pd.to_numeric(df['amount'], errors='coerce')
    df['order_date'] = df['order_date'].str.replace(
        r'(\d{2})/(\d{2})/(\d{4})',
        r'\3-\2-\1', regex=True
    )
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['customer', 'amount', 'order_date'])
    df = df.drop_duplicates()
    return df
```

## Key methods
- str.title() — Title Case
- str.lower() — lowercase
- str.strip() — remove whitespace
- pd.to_numeric(errors='coerce') — invalid → NaN
- pd.to_datetime(errors='coerce') — invalid → NaT
- dropna(subset=[...]) — drop rows with missing values
- drop_duplicates() — remove duplicate rows
- .copy() — protect original dataframe

## Mixed date formats — regex fix
```python
df['date'] = df['date'].str.replace(
    r'(\d{2})/(\d{2})/(\d{4})',  # matches DD/MM/YYYY
    r'\3-\2-\1',                  # converts to YYYY-MM-DD
    regex=True
)
```

## duplicated() options
- keep='first' — mark all duplicates except first
- keep='last'  — mark all duplicates except last
- keep=False   — mark ALL occurrences including first

## Key insight
Always call .copy() before modifying — prevents changing original dataframe
Always convert data types BEFORE dropping nulls
Always strip whitespace BEFORE title/lower case

## Correct order
1. .copy() first
2. Fix casing
3. Strip whitespace
4. Convert data types
5. Fix dates
6. Drop nulls
7. Drop duplicates
