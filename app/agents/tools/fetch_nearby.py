from app.db.crud import get_nearby_responders, get_nearby_hospitals
from geopy.geocoders import Nominatim
from google.adk.tools import FunctionTool

def fetch_location_info(lat: float, lng: float) -> dict:
    geolocator = Nominatim(user_agent="emergency_response_app")
    location = geolocator.reverse((lat, lng), language='en')
    print("Finding")
    if location and location.raw and 'address' in location.raw:
        address = location.raw['address']
        return {
            "city": address.get("city") or address.get("town") or address.get("village"),
            "state": address.get("state"),
            "country": address.get("country"),
            "postcode": address.get("postcode")
        }
    return {}

fetch_location_info_tool = FunctionTool(func=fetch_location_info)
get_nearby_responders_tool = FunctionTool(func=get_nearby_responders)
get_nearby_hospitals_tool = FunctionTool(func=get_nearby_hospitals)