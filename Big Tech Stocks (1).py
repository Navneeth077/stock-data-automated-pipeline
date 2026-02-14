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


import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import os


db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)

print("✅ Engine created. Ready to connect.")


# In[5]:


# Define the companies we want to track
tickers = ["AAPL", "MSFT", "GOOGL", "NVDA"]

# Download data from Yahoo Finance
raw_data = yf.download(tickers, period="1mo", interval="1d")

# Let's see what we got
raw_data.head()


# In[6]:


# 1. Grab only the 'Close' prices
df = raw_data['Close'].stack().reset_index()

# 2. Rename columns to be SQL-friendly (lowercase, no spaces)
df.columns = ['date', 'ticker', 'price_usd']

# 3. Clean any empty rows
df = df.dropna()

# Show the cleaned version
print("Cleaned Data Preview:")
print(df.tail())


# In[8]:


# Send to Neon. 'replace' will overwrite, 'append' will add to it.
df.to_sql('stock_prices_daily', engine, if_exists='replace', index=False)

print("🚀 Success! Your data is now in the cloud.")


# In[ ]:




