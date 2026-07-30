import time
import json
import redis
import yfinance as yf

r = redis.Redis(
    host="redis-cache",
    port=6379,
    decode_responses=True,
)

tickers = [
    "AAPL",
    "MSFT",
    "NVDA",
    "TSLA",
    "AMZN"
]

while True:

    for ticker in tickers:

        df = yf.Ticker(ticker).history(
            period="1d",
            interval="1m"
        )

        if df.empty:
            continue

        price = float(df["Close"].iloc[-1])

        r.xadd(
            "stream:prices",
            {
                "data": json.dumps({
                    "ticker": ticker,
                    "price": price
                })
            }
        )

        print(ticker, price)

    time.sleep(5)
