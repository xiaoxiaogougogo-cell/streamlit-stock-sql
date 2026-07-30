from fastapi import APIRouter

router = APIRouter()

@router.get("/orders")
async def orders():
    return {"message": "orders endpoint"}
