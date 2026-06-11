# Mini Project — Sales Analysis Report

## Overview
End-to-end sales analysis pipeline built in Python.
Takes raw messy data, cleans it, analyses it,
visualises it and exports to Excel automatically.

## Pipeline steps
1. Clean — fixes casing, whitespace, data types, dates, missing values
2. Transform — adds month and order size columns
3. Analyse — generates 4 summary tables
4. Visualise — creates 4 charts in one dashboard
5. Export — saves to timestamped Excel with 5 sheets

## Key findings
- Melbourne is the top city by revenue ($4,895)
- Laptop dominates product revenue ($7,200 — 83% of total)
- Premium segment spends more per customer than Standard
- May 2024 had a significant revenue dip worth investigating

## Tools used
- Python 3.12
- pandas — data cleaning and analysis
- matplotlib + seaborn — visualisation
- openpyxl — Excel export
- Google Colab

## How to run
1. Open in Google Colab
2. Run all cells
3. Download the generated Excel report
