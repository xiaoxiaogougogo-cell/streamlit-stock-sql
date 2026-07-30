







from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api.v1.metrics import router as metrics_router
from app.middleware.middleware import LoggingMiddleware
from app.api.v1.health import router as health_router
from app.api.v1.orders import router as orders_router
from app.api.v1.portfolio import router as portfolio_router


app = FastAPI()


@app.get("/")
async def root():
    return {
        "service": "Trading API",
        "status": "running"
    }

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["health"]
)



app.include_router(
    metrics_router,
    prefix="/api/v1",
    tags=["metrics"]
)



app.include_router(
    orders_router,
    prefix="/api/v1",
    tags=["orders"]
)

app.include_router(
    portfolio_router,
    prefix="/api/v1",
    tags=["portfolio"]
)

app.include_router(metrics_router)



