mport redis
import json

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def execute_order(order):
    print("EXECUTING:", order)
    # broker API call here

while True:
    msgs = r.xread({"stream:orders": "$"}, block=0)

    for stream, entries in msgs:
        for msg_id, msg in entries:
            order = json.loads(msg["data"])
            execute_order(order)
