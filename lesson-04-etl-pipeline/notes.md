# Lesson 4 — ETL Pipeline & Automation

## ETL concept
- Extract — load raw data
- Transform — clean and prepare
- Load — export results

## Full pipeline structure
```python
def extract(data):
    return data.copy()

def transform(df):
    df = df[df['status'] == 'completed'].copy()
    df['month'] = df['order_date'].dt.strftime('%Y-%m')
    df['size']  = df['amount'].apply(label_func)
    return df

def analyse(df):
    city_summary    = df.groupby('city').agg(...).reset_index()
    product_summary = df.groupby('product').agg(...).reset_index()
    month_summary   = df.groupby('month').agg(...).reset_index()
    return city_summary, product_summary, month_summary

def export(city, product, month, clean):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename  = f'report_{timestamp}.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        city.to_excel(writer,    sheet_name='By City',    index=False)
        product.to_excel(writer, sheet_name='By Product', index=False)
        month.to_excel(writer,   sheet_name='Monthly',    index=False)
        clean.to_excel(writer,   sheet_name='Raw Data',   index=False)
    return filename

def run_pipeline(data):
    raw                  = extract(data)
    clean                = transform(raw)
    city, product, month = analyse(clean)
    filename             = export(city, product, month, clean)
    return city, product, month, clean
```

## Key concepts
- ETL = Extract, Transform, Load
- pd.ExcelWriter — write multiple sheets to one Excel file
- with ... as: — context manager, auto closes file
- datetime.now().strftime() — timestamped filenames
- index=False — don't write row numbers to Excel
- .pipe() — chain functions cleanly
- glob.glob('*.csv') — find files matching pattern
- pd.concat([...]) — combine multiple dataframes

## apply vs pipe
- apply() — for simple functions on values/rows
- pipe()  — for functions on whole dataframe
- direct call clean(df) — always works for anything

## Key rules
- Name parameter 'row' not 'df' when using axis=1
- Use .copy() in every function to protect original
- reset_index() after groupby — proper column names
- index=False when exporting — no row numbers
