from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "emergency")

async def main():
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        
        # Seed Hospitals with GeoJSON locations
        hospitals = [
            {
                "name": "Central Hospital",
                "location": {
                    "type": "Point",
                    "coordinates": [-74.0060, 40.7128],  # [lng, lat]
                    "address": "123 Main St, New York, NY"
                },
                "beds_available": 50,
                "specialties": ["Emergency", "Cardiology", "Trauma"],
                "contact_phone": "+1234567890"
            },
            {
                "name": "City General Hospital",
                "location": {
                    "type": "Point", 
                    "coordinates": [-73.9857, 40.7484],
                    "address": "456 Health Ave, New York, NY"
                },
                "beds_available": 75,
                "specialties": ["Emergency", "Surgery", "Pediatrics"],
                "contact_phone": "+1234567891"
            },
            {
                "name": "Metro Medical Center",
                "location": {
                    "type": "Point",
                    "coordinates": [-74.0445, 40.6892],
                    "address": "789 Care Blvd, Brooklyn, NY"
                },
                "beds_available": 40,
                "specialties": ["Emergency", "Neurology", "Orthopedics"],
                "contact_phone": "+1234567892"
            }
        ]
        await db.hospitals.insert_many(hospitals)

        # Seed Responders (Ambulances/Paramedics) with GeoJSON locations
        responders = [
            {
                "name": "Ambulance Unit 1",
                "phone": "+1234567893",
                "location": {
                    "type": "Point",
                    "coordinates": [-74.0060, 40.7128]            },
                "status": "available",
                "vehicle_type": "ambulance",
                "skills": ["CPR", "Defibrillation", "IV Therapy"]
            },
            {
                "name": "Paramedic Team A",
                "phone": "+1234567894", 
                "location": {
                    "type": "Point",
                    "coordinates": [-73.9857, 40.7484]            },
                "status": "available",
                "vehicle_type": "paramedic",
                "skills": ["Advanced Life Support", "Trauma Care"]
            },
            {
                "name": "Ambulance Unit 2",
                "phone": "+1234567895",
                "location": {
                    "type": "Point", 
                    "coordinates": [-74.0445, 40.6892]            },
                "status": "available",
                "vehicle_type": "ambulance",
                "skills": ["CPR", "Basic Life Support"]
            }
        ]
        await db.responders.insert_many(responders)

        # Seed Sample Incidents (for testing)
        incidents = [
            {
                "caller_name": "John Doe",
                "caller_phone": "+1234567896",
                "incident_type": "chest_pain",
                "symptoms": "Severe chest pain, shortness of breath",
                "location": {
                    "lat": 40.7128,
                    "lng": -74.0060,
                    "address": "456 Emergency St, New York, NY"
                },
                "priority": "P2",
                "status": "active",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "caller_name": "Jane Smith", 
                "caller_phone": "+1234567897",
                "incident_type": "cardiac_arrest",
                "symptoms": "Unconscious, not breathing",
                "location": {
                    "lat": 40.7484,
                    "lng": -73.9857,
                    "address": "789 Crisis Ave, New York, NY"
                },
                "priority": "P1",
                "status": "dispatched",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        await db.incidents.insert_many(incidents)

        # Seed Sample Responses (linking incidents to responders)
        responses = [
            {
                "incident_id": "sample_incident_id_1",  # Replace with actual ObjectId after insertion
                "responder_id": "sample_responder_id_1",
                "eta": 8,
                "status": "en_route",
                "created_at": datetime.now(timezone.utc)
            }
        ]
        await db.responses.insert_many(responses)

        # Create geospatial indexes for efficient location queries
        await db.hospitals.create_index([("location", "2dsphere")])
        await db.responders.create_index([("location", "2dsphere")])

        print("Emergency system seeding complete!")
        print(f"Seeded {len(hospitals)} hospitals, {len(responders)} responders, {len(incidents)} incidents")

    except Exception as e:
        print(f"MongoDB connection error: {e}")
        print("Ensure MongoDB is running and credentials are correct.")
        return

if __name__ == "__main__":
    asyncio.run(main())