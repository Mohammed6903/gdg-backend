from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Hospital(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    location: Dict[str, float]  # {"lat": float, "lng": float}
    address: str
    beds_available: int = 0
    specialties: List[str] = []  # e.g., ["emergency", "cardiology"]
    contact_phone: str
    status: str = "operational"  # operational, overloaded, closed