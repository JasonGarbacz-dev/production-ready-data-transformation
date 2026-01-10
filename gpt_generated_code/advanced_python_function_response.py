import pandas as pd
import time
from datetime import datetime


def summarize_sales_data(file_path: str = "./data/sales.csv", debug: bool = True) -> None:
    """
    Summarize sales performance by product, customer, and month.

    This function reads a CSV file of sales transactions, filters for completed
    orders, and calculates three key summaries:
        1. Total sales by product_code
        2. Total sales by customer_id
        3. Monthly total sales based on the transaction date

    The results are printed cleanly to the terminal.

    Parameters
    ----------
    file_path : str, optional
        Path to the sales CSV file. Default is './data/sales.csv'.
    debug : bool, optional
        If True, prints detailed debug logs. Default is True.

    Returns
    -------
    None
        The function prints summaries to stdout and does not return a value.

    Raises
    ------
    FileNotFoundError
        If the CSV file cannot be located at the specified path.
    ValueError
        If required columns are missing from the CSV file.
    """

    start_time = time.time()
    if debug:
        print(f"[{datetime.now()}] Starting sales summary process...")
        print(f"Attempting to load data from: {file_path}")

    # Load CSV
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not find the file at {file_path}") from e

    # Validate expected columns
    required_cols = {
        "order_number",
        "customer_id",
        "transaction_amount",
        "date",
        "product_code",
        "status",
    }

    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"The following required columns are missing: {missing}")

    if debug:
        print(f"✅ Successfully loaded {len(df)} rows.")
        print("Filtering to completed transactions only...")

    # Filter for completed transactions
    df = df[df["status"].str.lower() == "completed"]

    if debug:
        print(f"Remaining rows after filtering: {len(df)}")

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows with invalid or missing dates
    df = df.dropna(subset=["date"])

    # --- Summaries ---
    if debug:
        print("Computing total sales by product_code...")
    sales_by_product = df.groupby("product_code")["transaction_amount"].sum().sort_values(ascending=False)

    if debug:
        print("Computing total sales by customer_id...")
    sales_by_customer = df.groupby("customer_id")["transaction_amount"].sum().sort_values(ascending=False)

    if debug:
        print("Computing monthly total sales...")
    df["month"] = df["date"].dt.to_period("M")
    monthly_sales = df.groupby("month")["transaction_amount"].sum().sort_index()

    # --- Output ---
    print("\n" + "=" * 60)
    print("📦 TOTAL SALES BY PRODUCT CODE")
    print("=" * 60)
    print(sales_by_product.to_string())

    print("\n" + "=" * 60)
    print("👤 TOTAL SALES BY CUSTOMER ID")
    print("=" * 60)
    print(sales_by_customer.to_string())

    print("\n" + "=" * 60)
    print("🗓️  MONTHLY TOTAL SALES")
    print("=" * 60)
    print(monthly_sales.to_string())

    runtime = time.time() - start_time
    print(f"\n✅ Sales summary completed in {runtime:.2f} seconds.\n")


# --- Optional: Run directly from terminal ---
if __name__ == "__main__":
    summarize_sales_data()
