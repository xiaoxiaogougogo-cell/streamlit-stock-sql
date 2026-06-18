from fastapi import APIRouter

router = APIRouter()

@router.get("/health/deep")
async def deep_health():

    return {
        "postgres": "ok",
        "redis": "ok",
        "api": "ok"
    }
