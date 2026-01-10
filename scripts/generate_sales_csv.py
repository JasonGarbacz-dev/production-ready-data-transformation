import csv
import os
import random
from datetime import datetime, timedelta
from typing import List, Tuple, Union


def generate_sales_csv(
    output_path: str = "data/sales.csv",
    num_rows: int = 50,
    start_date: datetime = datetime(2023, 11, 1),
    debug: bool = True
) -> str:
    """Generate a synthetic sales dataset and write it to a CSV file.

    This function creates randomized sales records for testing or demo purposes,
    including a few intentionally malformed rows to test data validation workflows.

    Args:
        output_path (str): Path where the CSV file will be written.
        num_rows (int): Number of valid rows to generate before adding malformed ones.
        start_date (datetime): Starting date for randomly generated sales dates.
        debug (bool, optional): If True, prints detailed debug information. Defaults to True.

    Returns:
        str: The absolute path to the generated CSV file.

    Raises:
        OSError: If there is an issue creating directories or writing the file.
    """
    start_time = datetime.now()
    if debug:
        print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 🔧 Starting CSV generation...")

    # === Configuration ===
    product_codes: List[str] = ["PRD-A12", "PRD-B07", "PRD-C03", "PRD-D55"]
    statuses: List[str] = ["Completed", "Canceled"]

    # === Step 1: Ensure output directory exists ===
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if debug:
            print(f"📂 Directory ensured: {os.path.dirname(output_path)}")
    except OSError as e:
        raise OSError(f"Failed to create output directory: {e}")

    # === Step 2: Generate valid rows ===
    rows: List[List[Union[str, float]]] = []
    if debug:
        print("🧪 Generating valid sales rows...")

    for i in range(num_rows):
        if debug and i % 10 == 0:
            print(f"  ...generating row {i}/{num_rows}")

        order_number = f"ORD-{1001 + i}"
        customer_id = f"CUST-{200 + random.randint(1, 20)}"
        date = start_date + timedelta(days=random.randint(0, 59))
        product_code = random.choice(product_codes)
        amount = round(random.uniform(20.0, 500.0), 2)
        status = random.choices(statuses, weights=[0.85, 0.15])[0]

        rows.append([
            order_number,
            customer_id,
            amount,
            date.strftime("%Y-%m-%d"),
            product_code,
            status,
        ])

    # === Step 3: Add malformed rows ===
    if debug:
        print("➕ Adding malformed rows...")
    malformed_rows: List[List[Union[str, float]]] = [
        ["ORD-9999", "CUST-999", "not_a_number", "2023-12-10", "PRD-A12", "Completed"],
        ["ORD-1000", "CUST-998", 400.00, "bad_date", "PRD-B07", "Completed"],
        ["ORD-1001", "CUST-997", 275.00, "2023-12-12", "", "Completed"],
    ]
    rows.extend(malformed_rows)

    # === Step 4: Write rows to CSV ===
    try:
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["order_number", "customer_id", "transaction_amount", "date", "product_code", "status"]
            )
            writer.writerows(rows)

        if debug:
            print(f"💾 Wrote {len(rows)} records (including malformed) to {output_path}")

    except OSError as e:
        raise OSError(f"Error writing to CSV file: {e}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"✅ CSV generation complete. ({duration:.2f}s) → {output_path}")

    return os.path.abspath(output_path)
