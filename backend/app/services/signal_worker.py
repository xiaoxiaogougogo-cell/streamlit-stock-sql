


import redis
import json

r = redis.Redis(host="redis-cache", port=6379, decode_responses=True)

msg_id = r.xadd(
    "stream:signals",
    {
        "data": json.dumps({
            "ticker": "AAPL",
            "action": "BUY",
            "confidence": 0.1
        })
    }
)

print("Published:", msg_id)
print("Length:", r.xlen("stream:signals"))
