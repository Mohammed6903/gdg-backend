from app.db.crud import (
    get_ambulance,
    create_ambulance,
    get_ambulance_assignment,
    get_ambulance_assignments_by_ambulance,
    get_ambulances_by_hospital,
    update_ambulance_location,
    update_ambulance_status,
    assign_ambulance_to_incident,
)
from google.adk.tools import FunctionTool

get_ambulance_tool = FunctionTool(get_ambulance)
create_ambulance_tool = FunctionTool(create_ambulance)
get_ambulance_assignment_tool = FunctionTool(get_ambulance_assignment)
get_ambulance_assignments_by_ambulance_tool = FunctionTool(get_ambulance_assignments_by_ambulance)
get_ambulances_by_hospital_tool = FunctionTool(get_ambulances_by_hospital)
update_ambulance_location_tool = FunctionTool(update_ambulance_location)
update_ambulance_status_tool = FunctionTool(update_ambulance_status)
assign_ambulance_to_incident_tool = FunctionTool(assign_ambulance_to_incident)
