from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Responder(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    phone: str
    location: Dict[str, float]  # {"lat": float, "lng": float}
    status: str = "available"  # available, en_route, busy, offline
    vehicle_type: str  # ambulance, paramedic, fire_truck
    skills: List[str] = []  # e.g., ["CPR", "trauma"]
    eta_to_incident: Optional[int] = None  # minutes