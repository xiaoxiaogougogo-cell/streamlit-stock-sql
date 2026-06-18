import redis.asyncio as redis
import os

redis_client = None

async def init_redis():

    global redis_client

    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=6379,
        decode_responses=True
    )
