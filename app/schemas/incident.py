from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class Incident(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    caller_name: Optional[str]
    caller_phone: Optional[str]
    incident_type: Optional[str]  # e.g., "medical", "accident"
    symptoms: Optional[str]
    summary: Optional[str]
    location: Dict[str, float]  # {"lat": float, "lng": float}
    address: Optional[str]
    priority: Optional[str] = "P3"  # P1 (critical), P2 (urgent), P3 (standard)
    status: str = "active"  # active, resolved, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_responder_id: Optional[str] = None