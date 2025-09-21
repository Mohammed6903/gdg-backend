from app.db.crud import get_hospital, get_all_hospitals, get_nearby_hospitals
from google.adk.tools import FunctionTool

get_hospital_tool = FunctionTool(get_hospital)
get_all_hospitals_tool = FunctionTool(get_all_hospitals)
get_nearby_hospitals_tool = FunctionTool(get_nearby_hospitals)