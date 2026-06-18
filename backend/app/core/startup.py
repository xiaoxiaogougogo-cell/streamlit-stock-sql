import asyncio
from sqlalchemy import text
from app.db.postgres import engine

async def wait_for_db():

    for attempt in range(30):

        try:

            async with engine.connect() as conn:

                await conn.execute(text("SELECT 1"))

                print("Database connected")

                return

        except Exception:

            print(f"Waiting for DB ({attempt+1}/30)")

            await asyncio.sleep(2)

    raise RuntimeError("Database unavailable")
