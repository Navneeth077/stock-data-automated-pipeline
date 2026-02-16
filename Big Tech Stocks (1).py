#!/usr/bin/env python
# coding: utf-8

"""
Automated Financial Data Pipeline
Extracts stock data, calculates indicators,
and stores it in Neon PostgreSQL.
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
    raw_data = yf.download(tickers, period="3mo", interval="1d")

    # Extract Close prices only
    close_data = raw_data["Close"]

    # Convert wide format to long format
    df = close_data.stack().reset_index()
    df.columns = ["date", "ticker", "close"]

    df = df.sort_values(["ticker", "date"])

    # 📈 Calculate indicators per ticker
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    df["sma_20"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(window=20).mean()
    )
    df["sma_50"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(window=50).mean()
    )
    df["volatility"] = df.groupby("ticker")["daily_return"].transform(
        lambda x: x.rolling(window=20).std()
    )

    # Drop rows that don't have enough data for indicators
    df = df.dropna()

    print("📊 Preview with Indicators:")
    print(df.tail())

    # Upload to database
    df.to_sql(
        "stock_prices_daily",
        engine,
        if_exists="replace",
        index=False
    )

    print("🚀 Data with indicators uploaded successfully!")


if __name__ == "__main__":
    main()


