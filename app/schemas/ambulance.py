from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class AmbulanceBase(BaseModel):
    hospital_id: str
    address: str
    contact_phone: str
    status: str = "operational"  # operational, overloaded, closed
    vehicle_number: str
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    equipment: Optional[List[str]] = []
    capacity: int = 1  # number of patients it can carry
    current_location: Optional[Dict[str, float]] = None  # {"lat": 0.0, "lng": 0.0}

class Ambulance(AmbulanceBase):
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AmbulanceStatusUpdate(BaseModel):
    status: str
    current_location: Optional[Dict[str, float]] = None

class AmbulanceLocationUpdate(BaseModel):
    current_location: Dict[str, float]  # {"lat": 0.0, "lng": 0.0"}

class AmbulanceAssignment(BaseModel):
    ambulance_id: str
    incident_id: str
    hospital_id: str
    estimated_arrival: Optional[datetime] = None
    status: str = "assigned"  # assigned, en_route, arrived, completed