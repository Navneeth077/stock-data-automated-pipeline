📈 Automated Stock Market ETL Pipeline
A production-grade, serverless data pipeline that extracts daily market data, transforms it for analysis, and loads it into a cloud PostgreSQL database.

🛠️ Technology Stack
Language: Python 3.11

Orchestration: GitHub Actions (Cron-scheduled)

Storage: Neon Cloud PostgreSQL

BI Tooling: Power BI (via PostgreSQL Connector)

Libraries: yfinance, pandas, sqlalchemy, psycopg2-binary

⚙️ Architecture & Data Flow
Extraction: A GitHub Action triggers daily (9:00 AM UTC) to fetch data from the Yahoo Finance API.

Transformation: Python handles data cleaning, using pandas to structure the time-series data and sqlalchemy for database communication.

Loading (Upsert): The pipeline uses a "Smart Sync" logic (ON CONFLICT). This ensures that if the script runs twice, it updates existing records instead of creating duplicates.

Security: Sensitive database credentials (connection strings) are encrypted and managed via GitHub Repository Secrets.

🚀 Key Features
Serverless & Cost-Free: Runs entirely on GitHub's infrastructure and Neon's free tier.

Idempotent Design: Prevents data duplication through SQL constraints and Python logic.

Auto-Refreshing Dashboard: Connected to Power BI for real-time visualization of stock trends.

📊 SQL Sample
To verify the data in the Neon SQL editor, run: SELECT * FROM stock_prices_daily;
