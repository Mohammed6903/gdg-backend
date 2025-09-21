from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Dict
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from app.db.session import get_db

# User operations (kept from original)
async def get_user(user_id: str):
    db = await get_db()
    return await db.users.find_one({"_id": ObjectId(user_id)})

async def create_user(data: dict):
    db = await get_db()
    result = await db.users.insert_one(data)
    return await db.users.find_one({"_id": result.inserted_id})

async def get_user_by_email(email: str):
    db = await get_db()
    return await db.users.find_one({"email": email})

# Incident operations
async def create_incident(data: dict):
    db = await get_db()
    data["created_at"] = datetime.now(timezone.utc)
    data["updated_at"] = datetime.now(timezone.utc)
    result = await db.incidents.insert_one(data)
    return await db.incidents.find_one({"_id": result.inserted_id})

async def get_incident(incident_id: str):
    db = await get_db()
    return await db.incidents.find_one({"_id": ObjectId(incident_id)})

async def get_latest_incident():
    db = await get_db()
    five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
    incident = await db.incidents.find_one(
        {"created_at": {"$gte": five_minutes_ago}},
        sort=[("created_at", -1)]
    )
    return incident

async def update_incident(incident_id: str, update_data: dict):
    db = await get_db()
    update_data["updated_at"] = datetime.now(timezone.utc)
    await db.incidents.update_one(
        {"_id": ObjectId(incident_id)}, 
        {"$set": update_data}
    )
    return await db.incidents.find_one({"_id": ObjectId(incident_id)})

async def get_active_incidents(limit: int = 50):
    db = await get_db()
    return await db.incidents.find({"status": "active"}).limit(limit).to_list(length=limit)

# Responder operations
async def get_nearby_responders(
    lat: float, lng: float, 
    radius: float = 10.0, vehicle_type: Optional[str] = None,
    max_results: int = 10, available_only: bool = True
) -> List[Dict]:
    db = await get_db()
    # Create base match conditions
    match_conditions = {}
    if available_only:
        match_conditions["status"] = "available"
    if vehicle_type:
        match_conditions["vehicle_type"] = vehicle_type

    # MongoDB geospatial aggregation pipeline
    pipeline = [
        {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": [lng, lat]},
                "distanceField": "distance_meters",
                "maxDistance": radius * 1000,  # Convert km to meters
                "spherical": True
            }
        },
        {"$match": match_conditions},
        {"$limit": max_results}
    ]

    results = await db.responders.aggregate(pipeline).to_list(length=max_results)
    
    # Add distance in km and estimated ETA
    responders = []
    for doc in results:
        doc["distance_km"] = doc["distance_meters"] / 1000
        # Simple ETA calculation (distance_km / average_speed * 60)
        # Assuming average emergency response speed of 40 km/h
        doc["eta_minutes"] = int((doc["distance_km"] / 40) * 60)
        responders.append(doc)
    
    return responders

async def create_responder(data: dict):
    db = await get_db()
    result = await db.responders.insert_one(data)
    return await db.responders.find_one({"_id": result.inserted_id})

async def update_responder_status(responder_id: str, status: str):
    db = await get_db()
    await db.responders.update_one(
        {"_id": ObjectId(responder_id)}, 
        {"$set": {"status": status}}
    )
    return await db.responders.find_one({"_id": ObjectId(responder_id)})

async def get_responder(responder_id: str):
    db = await get_db()
    return await db.responders.find_one({"_id": ObjectId(responder_id)})

# Hospital operations
async def get_nearby_hospitals(
    lat: float, lng: float,
    radius: float = 20.0, specialty: Optional[str] = None,
    beds_required: int = 1, max_results: int = 5
) -> List[Dict]:
    db = await get_db()
    # Create match conditions
    match_conditions = {"status": "operational", "beds_available": {"$gte": beds_required}}
    if specialty:
        match_conditions["specialties"] = {"$in": [specialty]}

    pipeline = [
        {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": [lng, lat]},
                "distanceField": "distance_meters",
                "maxDistance": radius * 1000,
                "spherical": True
            }
        },
        {"$match": match_conditions},
        {"$sort": {"distance_meters": 1}},
        {"$limit": max_results}
    ]

    results = await db.hospitals.aggregate(pipeline).to_list(length=max_results)
    
    # Add distance in km
    hospitals = []
    for doc in results:
        doc["distance_km"] = doc["distance_meters"] / 1000
        hospitals.append(doc)
    
    return hospitals

async def create_hospital(data: dict):
    db = await get_db()
    result = await db.hospitals.insert_one(data)
    return await db.hospitals.find_one({"_id": result.inserted_id})

async def update_hospital_beds(hospital_id: str, beds_available: int):
    db = await get_db()
    await db.hospitals.update_one(
        {"_id": ObjectId(hospital_id)}, 
        {"$set": {"beds_available": beds_available}}
    )
    return await db.hospitals.find_one({"_id": ObjectId(hospital_id)})

async def get_hospital(hospital_id: str):
    db = await get_db()
    return await db.hospitals.find_one({"_id": ObjectId(hospital_id)})

# Response operations
async def create_response(data: dict):
    db = await get_db()
    data["created_at"] = datetime.now(timezone.utc)
    result = await db.responses.insert_one(data)
    return await db.responses.find_one({"_id": result.inserted_id})

async def get_response(response_id: str):
    db = await get_db()
    return await db.responses.find_one({"_id": ObjectId(response_id)})

async def get_responses_by_incident(incident_id: str):
    db = await get_db()
    return await db.responses.find({"incident_id": incident_id}).to_list(length=None)

async def update_response_status(response_id: str, status: str):
    db = await get_db()
    await db.responses.update_one(
        {"_id": ObjectId(response_id)}, 
        {"$set": {"status": status}}
    )
    return await db.responses.find_one({"_id": ObjectId(response_id)})

# Utility functions for emergency management
async def get_dashboard_stats():
    db = await get_db()
    active_incidents = await db.incidents.count_documents({"status": "active"})
    available_responders = await db.responders.count_documents({"status": "available"})
    busy_responders = await db.responders.count_documents({"status": {"$in": ["en_route", "busy"]}})
    
    return {
        "active_incidents": active_incidents,
        "available_responders": available_responders,
        "busy_responders": busy_responders,
        "total_responders": available_responders + busy_responders
    }

async def assign_responder_to_incident(incident_id: str, responder_id: str):
    db = await get_db()
    # Update incident with assigned responder
    await db.incidents.update_one(
        {"_id": ObjectId(incident_id)}, 
        {"$set": {"assigned_responder_id": responder_id, "updated_at": datetime.now(timezone.utc)}}
    )
    
    # Update responder status
    await db.responders.update_one(
        {"_id": ObjectId(responder_id)}, 
        {"$set": {"status": "en_route"}}
    )
    
    # Create response record
    response_data = {
        "incident_id": incident_id,
        "responder_id": responder_id,
        "status": "dispatched"
    }
    return await create_response(response_data)