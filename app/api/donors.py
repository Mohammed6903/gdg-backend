# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.db.crud import get_nearby_donors
# from fastapi import Depends
# from typing import Dict, Optional, List
# from app.db.session import get_db
# from app.schemas.donor import Donor
# from prisma import Prisma

# router = APIRouter()

# class NearbyRequest(BaseModel):
#     lng: float
#     lat: float
#     radius: Optional[int] = 10

# @router.post("/nearby-donors")
# async def get_nearby_donors_api(
#     req: NearbyRequest,
#     db: Prisma = Depends(get_db)
# ):
#     donors: List[Donor] = await get_nearby_donors(
#         lng=req.lng,
#         lat=req.lat,
#         radius=req.radius,
#         db=db
#     )
#     return donors