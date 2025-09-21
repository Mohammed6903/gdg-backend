from fastapi import APIRouter
from app.db.crud import get_latest_incident

router = APIRouter()

@router.get("/")
async def get_incident():
    return await get_latest_incident()