


from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()
import os

DB_HOST = os.getenv("POSTGRES_HOST")

from dotenv import load_dotenv

load_dotenv()

from app.routes.health import router as health_router
from app.routes.metrics import router as metrics_router

app = FastAPI()


@app.get("/")
async def root():
    return {
        "service": "Trading API",
        "status": "running"
    }

app.include_router(health_router)
app.include_router(metrics_router)
app.add_middleware(LoggingMiddleware)
