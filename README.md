# Production-Ready Python Data Transformation Pattern

This repository demonstrates my approach to designing production-aligned Python data transformation logic.

The example centers on a sales aggregation task, but the focus is not the aggregation itself — it’s the engineering standards applied to ensure reliability under real-world data conditions.

This project illustrates how I structure transformation functions to be:

- Modular and reusable  
- Explicit about business logic  
- Schema-aware  
- Fault-tolerant  
- Traceable through logging  
- Safe under imperfect input data  

While GPT-assisted code generation was used as an accelerator, the emphasis is on enforcing disciplined engineering patterns — not on the LLM itself.

---

## Engineering Standard

The transformation function implemented here includes:

- Explicit input validation
- Defensive type coercion (`errors="coerce"`)
- Graceful handling of malformed dates and mixed types
- Parameterization for reuse
- Structured logging and debug controls
- Deterministic output formatting
- No silent failures

The goal is not simply to “get correct output,” but to ensure predictable behavior under failure conditions.

---

## Example Business Scenario

Prompted task:

- Aggregate total sales by product_code  
- Aggregate total sales by customer_id  
- Compute monthly sales totals  
- Exclude non-completed transactions  

The implementation converts this business request into a reusable transformation function capable of:

- Validating schema assumptions
- Cleaning malformed data
- Logging row-level data loss
- Continuing execution without hard crashes
- Producing consistent structured output

---

## Behavior Under Imperfect Data

Two test scenarios are included:

### Clean Data

Both baseline GPT output and structured implementation produce correct results.

### Corrupted / Mixed-Type Data

Only the structured implementation:

- Coerces invalid dates safely
- Handles non-numeric transaction values
- Logs dropped rows explicitly
- Continues execution
- Produces final grouped outputs without terminating early

The focus is system behavior — not just correctness on ideal input.

---

## Why This Matters

In analytics engineering environments, most transformation logic does not fail on happy-path data.

It fails when:

- Date formats drift
- Numeric fields contain strings
- Schemas evolve
- Upstream systems introduce unexpected edge cases

This repository demonstrates a pattern for writing transformation logic that anticipates and absorbs those realities.

---

## Repo Structure

```bash
├── data/                    # Clean and error test CSVs
├── gpt_generated_code/      # Raw GPT-generated .py files (unchanged)
├── notebooks/               # Side-by-side validation notebooks
├── prompts/                 # Original prompt used
├── scripts/                 # Data generators
├── docs/                    # System instruction summary
└── README.md
```

---

## About

Built by **Jason Garbacz** — Senior Analytics Engineer focused on:

- Data workflow optimization  
- Transformation-layer engineering  
- Legacy-to-modern modernization  
- Internal tooling that improves reliability and delivery speed  

In modern analytics environments, generating Python is easy.

Designing transformation logic that survives real data is the differentiator.
