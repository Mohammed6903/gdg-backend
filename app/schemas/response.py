from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Response(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    incident_id: str
    responder_id: str
    eta: Optional[int]  # estimated time of arrival in minutes
    status: str = "dispatched"  # dispatched, en_route, arrived, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None