import time
import redis
from datetime import datetime
import os 
r = redis.Redis(
    host="redis-cache",
    port=6379,
    decode_responses=True
)





def publish_tick(ticker, price):
    print(f"Publishing: {ticker} {price}")

    msg_id = r.xadd(
        "market_ticks",
        {
            "ticker": ticker,
            "price": price,
            "time": datetime.now().isoformat()
        }
    )

    print(f"Redis message ID: {msg_id}")
