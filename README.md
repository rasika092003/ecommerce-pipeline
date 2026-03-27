# E-Commerce Data Pipeline

An end-to-end data engineering project that simulates a real-world e-commerce data pipeline using Python, PostgreSQL, dbt, and Apache Airflow.

---

## Architecture
```
Faker (Python) → PostgreSQL → dbt Models → Airflow DAGs → Astronomer Cloud
```

---

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11 | Data generation, ETL scripts |
| PostgreSQL | 18 | Local relational database |
| dbt-postgres | 1.11 | Data transformations + testing |
| Apache Airflow | 3.1.8 | Pipeline orchestration |
| Astronomer | Cloud | Managed Airflow deployment |

---

## Project Structure
```
ecommerce-pipeline/
├── scripts/
│   ├── create_schema.py        # Creates PostgreSQL tables
│   └── generate_data.py        # Generates fake e-commerce data
├── ecommerce_dbt/
│   ├── dbt_project.yml         # dbt configuration
│   └── models/
│       ├── staging/            # Raw → cleaned models
│       │   ├── stg_customers.sql
│       │   ├── stg_products.sql
│       │   ├── stg_orders.sql
│       │   ├── stg_order_items.sql
│       │   ├── stg_categories.sql
│       │   ├── sources.yml
│       │   └── schema.yml
│       └── marts/              # Business ready models
│           ├── dim_customers.sql
│           ├── dim_products.sql
│           ├── dim_date.sql
│           ├── fct_orders.sql
│           └── schema.yml
├── astro-project/
│   └── dags/
│       └── ecommerce_pipeline.py  # Airflow DAG
├── screenshots/
│   └── lineage_graph.png       # dbt lineage graph
└── README.md
```

---

## Data Model

### Raw Tables (PostgreSQL)

| Table | Rows | Description |
|-------|------|-------------|
| customers | 10,000 | Customer profiles |
| products | 500 | Product catalog |
| orders | 50,000 | Order transactions |
| order_items | ~125,000 | Order line items |
| categories | 6 | Product categories |

### Star Schema (dbt Marts)
```
                    dim_customers
                         │
dim_date ──────── fct_orders ──────── dim_products
```

| Model | Type | Rows | Description |
|-------|------|------|-------------|
| dim_customers | Table | 10,000 | Customers with lifetime value + segments |
| dim_products | Table | 500 | Products with sales performance |
| dim_date | Table | 1,826 | Date dimension (2022-2026) |
| fct_orders | Table | 50,000 | Central fact table |

---

## dbt Tests

26 data quality tests passing across all models:

| Test Type | What it checks |
|-----------|---------------|
| `unique` | No duplicate IDs |
| `not_null` | No missing values |
| `accepted_values` | Valid order status, segments |
```
dbt test result: PASS=26 WARN=0 ERROR=0
```

---

## Airflow Pipeline

Daily DAG with 4 tasks running in sequence:
```
generate_new_orders
        ↓
validate_data
        ↓
load_to_postgres
        ↓
run_dbt_models
```

| Task | Description |
|------|-------------|
| generate_new_orders | Simulates 500 new daily orders |
| validate_data | Checks data quality thresholds |
| load_to_postgres | Loads new data to database |
| run_dbt_models | Runs all dbt transformations |

---

## dbt Lineage Graph

![Lineage Graph](screenshots/lineage_graph.png)



## Project Progress

- [x] Month 1 — PostgreSQL schema + data generation + 10 SQL analysis queries
- [x] Month 2 — dbt star schema + 9 models + 26 data quality tests
- [x] Month 3 — Airflow DAG deployed on Astronomer Cloud
- [ ] Month 4 — GCP cloud deployment (BigQuery + Cloud Storage)

---

## Key Learnings

- Designed a normalized relational schema with 5 tables and proper foreign key relationships
- Built a star schema data warehouse using dbt with staging and mart layers
- Implemented data quality testing with 26 automated dbt tests
- Orchestrated a daily pipeline using Apache Airflow on Astronomer Cloud
- Used environment variables to securely manage database credentials
