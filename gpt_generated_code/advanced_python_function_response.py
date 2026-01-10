import pandas as pd
import time

def summarize_sales_data(file_path="./data/sales_with_errors.csv", debug=True):
    """
    Summarize sales data from a CSV file by product, customer, and month.

    This function loads order-level transaction data, filters for completed transactions,
    and generates the following summaries:
      1. Total sales grouped by product_code
      2. Total sales grouped by customer_id
      3. Monthly total sales based on the transaction date

    Parameters
    ----------
    file_path : str, optional
        Path to the CSV file containing sales data.
    debug : bool, optional
        If True, prints detailed logging of data loading, filtering, coercion, and aggregation steps.

    Returns
    -------
    None
        Prints summary tables to the console.

    Raises
    ------
    FileNotFoundError
        If the specified file_path cannot be found.
    ValueError
        If required columns are missing from the CSV.
    
    Example
    -------
    >>> summarize_sales_data("C:/data/sales_with_errors.csv", debug=True)
    """

    start_time = time.time()
    if debug:
        print(f"\n[INFO] Starting sales summary at {time.ctime(start_time)}")
        print(f"[INFO] Reading CSV file: {file_path}")

    # Load data
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    # Validate required columns
    required_cols = ["order_number", "customer_id", "transaction_amount", "date", "product_code", "status"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Filter completed transactions
    df = df[df["status"].str.lower() == "completed"]
    if debug:
        print(f"[DEBUG] Filtered to {len(df)} completed transactions.")

    # Coerce numeric values for transaction_amount
    df["transaction_amount"] = pd.to_numeric(df["transaction_amount"], errors="coerce")
    dropped_rows = df["transaction_amount"].isna().sum()
    df = df.dropna(subset=["transaction_amount"])
    if debug:
        if dropped_rows > 0:
            print(f"[DEBUG] Dropped {dropped_rows} rows with non-numeric transaction_amount values.")
        print("[DEBUG] Numeric coercion complete — calculations successful.")

    # Convert date to datetime and extract month
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month"] = df["date"].dt.to_period("M")

    # --- 1. Total sales by product_code ---
    sales_by_product = df.groupby("product_code")["transaction_amount"].sum().reset_index()
    sales_by_product = sales_by_product.sort_values(by="transaction_amount", ascending=False)

    # --- 2. Total sales by customer_id ---
    sales_by_customer = df.groupby("customer_id")["transaction_amount"].sum().reset_index()
    sales_by_customer = sales_by_customer.sort_values(by="transaction_amount", ascending=False)

    # --- 3. Monthly total sales ---
    monthly_sales = df.groupby("month")["transaction_amount"].sum().reset_index()
    monthly_sales = monthly_sales.sort_values(by="month")

    # Print results to console
    print("\n===== TOTAL SALES BY PRODUCT =====")
    print(sales_by_product.to_string(index=False))
    print("\n===== TOTAL SALES BY CUSTOMER =====")
    print(sales_by_customer.to_string(index=False))
    print("\n===== MONTHLY SALES TOTALS =====")
    print(monthly_sales.to_string(index=False))

    # Runtime summary
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print(f"\n[INFO] Sales summary complete at {time.ctime(end_time)}")
    print(f"[INFO] Runtime: {duration} seconds")


if __name__ == "__main__":
    summarize_sales_data(debug=True)
