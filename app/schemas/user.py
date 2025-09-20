from pydantic import BaseModel, Field
from typing import Optional, Dict

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    phone: Optional[str]
    role: str  # dispatcher, responder, admin
    location: Optional[Dict[str, float]]  # {"lat": float, "lng": float}
    is_active: bool = True