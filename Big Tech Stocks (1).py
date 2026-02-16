#!/usr/bin/env python
# coding: utf-8

"""
Advanced Financial Data Pipeline
Downloads stock data, calculates technical indicators,
and uploads to Neon PostgreSQL.
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
    raw_data = yf.download(tickers, period="6mo", interval="1d")

    # Extract needed fields
    close = raw_data["Close"]
    volume = raw_data["Volume"]

    # Convert to long format
    df_close = close.stack().reset_index()
    df_volume = volume.stack().reset_index()

    df_close.columns = ["date", "ticker", "close"]
    df_volume.columns = ["date", "ticker", "volume"]

    df = pd.merge(df_close, df_volume, on=["date", "ticker"])
    df = df.sort_values(["ticker", "date"])

    # Handle missing volume safely
    df["volume"] = df["volume"].fillna(0).astype(int)

    # 📈 Daily Return
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()

    # 📊 Moving Averages
    df["sma_20"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(20).mean()
    )

    df["sma_50"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(50).mean()
    )

    # 📉 Volatility (20-day rolling std dev)
    df["volatility_20"] = df.groupby("ticker")["daily_return"].transform(
        lambda x: x.rolling(20).std()
    )

    # 🚀 Exponential Moving Average
    df["ema_20"] = df.groupby("ticker")["close"].transform(
        lambda x: x.ewm(span=20, adjust=False).mean()
    )

    # 📊 Rolling 30-Day High & Low
    df["rolling_30_high"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(30).max()
    )

    df["rolling_30_low"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(30).min()
    )

    # 📈 Price vs SMA Spread (Trend Strength)
    df["price_sma20_diff"] = df["close"] - df["sma_20"]

    # Remove incomplete rows
    df = df.dropna()

    print("📊 Final Preview:")
    print(df.tail())

    df.to_sql(
        "stock_prices_daily",
        engine,
        if_exists="replace",
        index=False
    )

    print("🚀 Advanced financial data uploaded successfully!")


if __name__ == "__main__":
    main()


