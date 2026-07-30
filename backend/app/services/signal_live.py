import pandas as pd
import json
import redis
r = redis.Redis(
    host="redis-cache",
    port=6379,
    decode_responses=True,
)

prices = []
last_id = "0"

print("Signal worker started")

while True:

    messages = r.xread(
        {"stream:prices": last_id},
        block=5000,
    )

    if not messages:
        continue

    for stream, entries in messages:

        for msg_id, fields in entries:

            last_id = msg_id

            data = json.loads(fields["data"])

            ticker = data["ticker"]
            price = float(data["price"])

            prices.append(price)

            if len(prices) < 20:
                continue

            df = pd.DataFrame({"price": prices})

            ma = df["price"].rolling(10).mean().iloc[-1]
            ema = df["price"].ewm(span=10).mean().iloc[-1]

            if ma > ema:
                signal = "BUY"
                confidence = 0.80
            elif ma < ema:
                signal = "SELL"
                confidence = 0.80
            else:
                signal = "HOLD"
                confidence = 0.50

            r.xadd(
                "stream:signals",
                {
                    "data": json.dumps({
                        "ticker": ticker,
                        "action": signal,
                        "confidence": confidence
                    })
                }
            )

            print(ticker, price, signal)
