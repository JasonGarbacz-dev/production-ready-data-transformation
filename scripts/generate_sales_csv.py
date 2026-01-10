import csv
import os
import random
from datetime import datetime, timedelta

# === Config ===
OUTPUT_PATH = "data/sales.csv"
NUM_ROWS = 50
START_DATE = datetime(2023, 11, 1)

# === Sample Values ===
product_codes = ["PRD-A12", "PRD-B07", "PRD-C03", "PRD-D55"]
statuses = ["Completed"]  # Only clean, successful transactions

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# === Generate Rows ===
rows = []
for i in range(NUM_ROWS):
    order_number = f"ORD-{1001 + i}"
    customer_id = f"CUST-{200 + random.randint(1, 20)}"
    date = START_DATE + timedelta(days=random.randint(0, 59))
    product_code = random.choice(product_codes)
    amount = float(round(random.uniform(20.0, 500.0), 2))  # Enforce float
    status = "Completed"

    rows.append([
        order_number,
        customer_id,
        amount,
        date.strftime("%Y-%m-%d"),
        product_code,
        status
    ])

# === Write CSV ===
with open(OUTPUT_PATH, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["order_number", "customer_id", "transaction_amount", "date", "product_code", "status"])
    writer.writerows(rows)

print(f"✅ Generated {len(rows)} clean sales records → {OUTPUT_PATH}")
