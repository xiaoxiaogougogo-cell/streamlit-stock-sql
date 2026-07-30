import redis

r = redis.Redis(
    host="redis-cache",
    port=6379,
    decode_responses=True
)
