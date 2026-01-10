# 🧠 Production-Ready Python Generator

Anyone can write Python with GPT — my GPT ships clean, production-aligned code by default.


This repo demonstrates a system-level difference between:

- 🤖 **Free ChatGPT (GPT-3.5)** — functional, but brittle code generation
- 🧩 **Custom GPT (Advanced Python Functions)** — production-ready Python by default

Both GPTs were given the *same* natural language prompt. Each produced working code on clean data. But when tested against real-world errors, only one recovered gracefully and offered traceable, correct results.

---

## 🎯 Purpose

This project benchmarks LLM-generated Python code using:
- ✅ Clean data
- ⚠️ Controlled bad data (invalid dates, mixed types, missing fields)

The goal: show how structured GPT behavior delivers code that’s:
- Modular
- Traceable
- Fault-tolerant
- Ready for reuse or extension

---

## 💬 The Prompt Used

```text
Hey — can you help me summarize some sales data?
We’ve got a CSV file with order-level transactions. I need you to generate python code for me to run locally to get at the following insights:

1. Total sales grouped by product_code  
2. Total sales grouped by customer_id  
3. Monthly sales totals based on the date column

You can skip rows where status isn’t "Completed" — we’re only looking at finalized transactions.

The file is located at ./data/sales.csv and includes these columns:
- order_number
- customer_id
- transaction_amount
- date
- product_code
- status

Just output everything to the terminal in a clean format — I’ll copy/paste it and run it locally.
```

---

## 🧪 Results on Clean Data

### ✅ ChatGPT Output (3.5)
```text
=== Total Sales by Product Code ===
product_code  transaction_amount
     PRD-C03             4988.34
     PRD-A12             3646.37
     PRD-B07             3089.68
     PRD-D55             2154.54
```

### ✅ Custom GPT Output
```text
📦 TOTAL SALES BY PRODUCT CODE
product_code
PRD-C03    4988.34
PRD-A12    3646.37
PRD-B07    3089.68
PRD-D55    2154.54
```

🟢 Both produce accurate results, but only the Custom GPT:
- Wraps logic in a reusable function
- Includes a `debug=True` parameter by default
- Logs runtime, row counts, and step checkpoints
- Validates schema and dates

---

## ⚠️ Results on Error Data (with mixed types, invalid dates, casing mismatches)

### ❌ ChatGPT Output
```text
ValueError: time data "12/31/2023" doesn't match format "%Y-%m-%d"
```
💥 Crashes on invalid date. No output.
🟥 ChatGPT never reaches the malformed transaction_amount field.
The first error halts execution, and there's no visibility into downstream data issues.

### ✅ Custom GPT Output
```text
[2026-01-10 14:29:12] Starting sales summary process...
✅ Successfully loaded 49 rows.
Filtering to completed transactions only...
✅ Coerced transaction_amount to numeric and dropped invalid rows.
Remaining rows after numeric cleaning: 47
Computing total sales by product_code...
...
✅ Sales summary completed in 0.01 seconds.
```

🧠 The Custom GPT:

✅ Coerced invalid dates using errors='coerce'
✅ Reached the non-numeric transaction_amount value
✅ Dropped malformed rows and logged row count
✅ Continued to produce accurate groupings
✅ Never failed silently or exited early

➡️ It didn’t just run — it gracefully handled multiple data issues on it's first version.

---

## 📁 Repo Structure

```bash
├── data/                          # Clean and error test CSVs
├── gpt_generated_code/           # Raw GPT-generated .py files (unchanged)
├── notebooks/                    # Side-by-side test notebooks
├── prompts/                      # Original prompt used
├── scripts/                      # Data generators
├── docs/                         # System instruction summary
└── README.md
```

---

## 🧠 What This Demonstrates

| Capability | ChatGPT | Custom GPT |
|------------|---------|------------|
| Working code on clean input | ✅ | ✅  |
| Modularity & function structure | ❌ | ✅  |
| Debug & runtime logging | ❌ | ✅  |
| Handles invalid data types | ❌ | ✅  |
| Explains what went wrong | ❌ | ✅  |
| Ready for production use | ❌ | ✅  |

---

## 🙋‍♂️ About

Built by **Jason Garbacz** — focused on:
- Internal tooling
- AI workflow integration
- Systems that replace ambiguity with clarity

> In the age of LLMs, anyone can generate Python.
> I build systems that generate Python you can ship.
