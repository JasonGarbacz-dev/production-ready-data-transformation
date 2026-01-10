# ChatGPT - Free 1/10/2026

import pandas as pd

# Load the CSV
df = pd.read_csv("./data/sales.csv")

# Ensure date column is parsed as datetime
df["date"] = pd.to_datetime(df["date"])

# Filter to completed transactions only
df_completed = df[df["status"] == "Completed"]

# 1. Total sales by product_code
sales_by_product = (
    df_completed
    .groupby("product_code", as_index=False)["transaction_amount"]
    .sum()
    .sort_values("transaction_amount", ascending=False)
)

# 2. Total sales by customer_id
sales_by_customer = (
    df_completed
    .groupby("customer_id", as_index=False)["transaction_amount"]
    .sum()
    .sort_values("transaction_amount", ascending=False)
)

# 3. Monthly sales totals
df_completed["month"] = df_completed["date"].dt.to_period("M")
monthly_sales = (
    df_completed
    .groupby("month", as_index=False)["transaction_amount"]
    .sum()
    .sort_values("month")
)

# Output results
print("\n=== Total Sales by Product Code ===")
print(sales_by_product.to_string(index=False))

print("\n=== Total Sales by Customer ID ===")
print(sales_by_customer.to_string(index=False))

print("\n=== Monthly Sales Totals ===")
print(monthly_sales.to_string(index=False))
