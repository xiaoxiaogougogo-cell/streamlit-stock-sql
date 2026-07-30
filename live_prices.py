
import yfinance as yf



import pandas as pd



from datetime import datetime

from backend.app.redis_stream import publish_tick

def fetch_live_price(ticker):
    data = yf.Ticker(ticker)
    df = data.history(period="1d", interval="1m")

    if df.empty:
        return None

    price = df["Close"].iloc[-1]

    publish_tick(ticker, price)

    return {
        "ticker": ticker,
        "price": price,
        "time": datetime.now()
    }

