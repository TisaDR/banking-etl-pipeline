# Banking ETL Pipeline

A data engineering pipeline built with Python, pandas, and PostgreSQL.

## What it does
- Extracts transaction data from CSV
- Transforms and cleans the data
- Loads clean data into PostgreSQL
- Runs automatically daily via Windows Task Scheduler

## Tech Stack
- Python 3.13
- PostgreSQL 18
- pandas
- SQLAlchemy
- psycopg2

## Scripts
- `etl_pipeline.py` — main ETL pipeline
- `generate_transactions.py` — generates fake transaction data
- `db_connect.py` — database connection and analysis

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Set up `.env` file with database credentials
3. Run: `python etl_pipeline.py`