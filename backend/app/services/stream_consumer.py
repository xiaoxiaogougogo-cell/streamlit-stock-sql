

import redis

r = redis.Redis(host="redis-cache", port=6379, decode_responses=True)

print("Connected:", r.ping())
print("Current stream length:", r.xlen("market_ticks"))

last_id = "0"

while True:
    print("Waiting for new ticks...")
    messages = r.xread({"market_ticks": last_id}, block=5000)

    print("Received:", messages)

    if not messages:
        continue

    for stream, entries in messages:
        for msg_id, fields in entries:
            print(msg_id, fields)
            last_id = msg_id
