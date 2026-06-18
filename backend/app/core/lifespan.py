from contextlib import asynccontextmanager
from app.db.postgres import init_postgres
from app.db.redis import init_redis

@asynccontextmanager
async def lifespan(app):

    await init_postgres()
    await init_redis()

    yield

    print("Shutting down cleanly...")
