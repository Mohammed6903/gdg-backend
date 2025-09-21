from app.db.crud import create_incident, update_incident, create_response
from google.adk.tools import FunctionTool
from app.schemas.incident import Incident

CreateIncidentTool = FunctionTool(func=create_incident)
UpdateIncidentTool = FunctionTool(func=update_incident)