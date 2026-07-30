import redis
import json

r = redis.Redis(host="redis-cache", port=6379, decode_responses=True)

def risk_check(signal):
    # simple rule (expand later)
    return signal["confidence"] > 0.7





last_id = "0"

print("Connected:", r.ping())
print("Signals:", r.xlen("stream:signals"))

while True:
    msgs = r.xread(
        {"stream:signals": last_id},
        block=5000,
    )

    print(msgs)

    if not msgs:
        continue

    for stream, entries in msgs:
        for msg_id, msg in entries:
            last_id = msg_id
            print(msg_id, msg)
