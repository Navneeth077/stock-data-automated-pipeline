#!/usr/bin/env python
# coding: utf-8

"""
Automated Financial Data Pipeline
Extracts stock data and stores it in Neon PostgreSQL.
"""

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import os


def main():
    db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set.")

    engine = create_engine(db_url)
    print("✅ Connected to database.")

    tickers = ["AAPL", "MSFT", "GOOGL", "NVDA"]

    print("📥 Downloading stock data...")
    raw_data = yf.download(tickers, period="1mo", interval="1d")

    df = raw_data["Close"].stack().reset_index()
    df.columns = ["date", "ticker", "price_usd"]
    df = df.dropna()

    print("📊 Preview:")
    print(df.tail())

    df.to_sql(
        "stock_prices_daily",
        engine,
        if_exists="replace",
        index=False
    )

    print("🚀 Data successfully uploaded!")


if __name__ == "__main__":
    main()

