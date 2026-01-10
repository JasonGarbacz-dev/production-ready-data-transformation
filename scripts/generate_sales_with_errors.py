import csv
import os
import random
from datetime import datetime, timedelta
from typing import List, Union


def generate_sales_with_errors_csv(
    output_path: str = "data/sales_with_errors.csv",
    num_rows: int = 45,
    start_date: datetime = datetime(2023, 11, 1),
    debug: bool = True
) -> str:
    """Generate a synthetic sales dataset with intentional data issues.

    This function creates a CSV file containing clean and malformed sales records,
    useful for testing data validation, cleaning, and aggregation logic.

    Args:
        output_path (str): Path to save the generated CSV file.
        num_rows (int): Number of valid (clean) rows to generate before adding malformed ones.
        start_date (datetime): Base date for generating random transaction dates.
        debug (bool): If True, prints debug logs to the console.

    Returns:
        str: The absolute path to the generated CSV file.

    Raises:
        OSError: If the output directory or file cannot be created or written.
    """
    start_time = datetime.now()
    if debug:
        print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 🧩 Starting sales data generation...")

    # --- Configuration ---
    product_codes: List[str] = ["PRD-A12", "PRD-B07", "PRD-C03", "PRD-D55"]
    statuses: List[str] = ["Completed"]

    # --- Ensure output directory exists ---
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if debug:
            print(f"📂 Directory ensured: {os.path.dirname(output_path)}")
    except OSError as e:
        raise OSError(f"Failed to create directory {os.path.dirname(output_path)}: {e}")

    rows: List[List[Union[str, float]]] = []

    # --- Generate clean rows ---
    if debug:
        print(f"🧮 Generating {num_rows} clean rows...")

    for i in range(num_rows):
        order_number = f"ORD-{2000 + i}"
        customer_id = f"CUST-{200 + random.randint(1, 20)}"
        amount = float(round(random.uniform(50.0, 500.0), 2))
        date_str = (start_date + timedelta(days=random.randint(0, 59))).strftime("%Y-%m-%d")
        product_code = random.choice(product_codes)
        status = "Completed"

        rows.append([order_number, customer_id, amount, date_str, product_code, status])

        if debug and i % 10 == 0:
            print(f"  ↳ Generated row {i}/{num_rows}")

    # --- Add intentional error rows ---
    if debug:
        print("⚠️ Injecting controlled data issues...")

    error_rows: List[List[Union[str, float]]] = [
        ["ORD-9991", "CUST-999", 199.99, "12/31/2023", "PRD-A12", "Completed"],  # Invalid date format
        ["ORD-9992", "CUST-998", "one_hundred", "2023-12-15", "PRD-B07", "Completed"],  # Non-numeric amount
        ["ORD-9993", "CUST-997", 275.00, "2023-12-12", "PRD-C03", "completed"],  # Status casing mismatch
        ["ORD-9994", "CUST-996", 134.00, "2023-12-18", "", "Completed"],  # Missing product_code
    ]
    rows.extend(error_rows)

    # --- Write to CSV ---
    try:
        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "order_number",
                "customer_id",
                "transaction_amount",
                "date",
                "product_code",
                "status"
            ])
            writer.writerows(rows)

        if debug:
            print(f"💾 Wrote {len(rows)} total rows ({len(error_rows)} malformed) → {output_path}")

    except OSError as e:
        raise OSError(f"Error writing to {output_path}: {e}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"✅ CSV generation complete in {duration:.2f}s → {output_path}")

    return os.path.abspath(output_path)
