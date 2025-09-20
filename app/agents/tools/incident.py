from app.db.crud import create_incident, create_response
from google.adk.tools import FunctionTool

CreateIncidentTool = FunctionTool(func=create_incident)