from fastapi import FastAPI
from database import users_collection, address_collection
from bson import ObjectId
import random
from aggregation import aggregation_route

app = FastAPI( 
    title="FastAPI + MongoDB",
    description="A simple FastAPI application demonstrating MongoDB integration with aggregation pipelines.",
    version="1.0.0",
)

@app.get("/", tags=["Root"])
def home():
    return {"message": "FastAPI + MongoDB Working 🚀"}


@app.post("/create-addresses", tags=["Create"])
def create_addresses():
    cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
              "Hyderabad", "Pune", "Allahabad", "Varanasi", "Lucknow"
    ]

    data = [{"city": city} for city in cities]
    address_collection.insert_many(data)

    return {"message": "Addresses inserted"}

@app.post("/insert-users", tags=["Create"])
def insert_users():
    addresses = list(address_collection.find())

    users = []

    for i in range(100):
        user = {
            "name": f"User{i}",
            "age": random.randint(15,75),
            "address_id": random.choice(addresses)["_id"]
        }
        users.append(user)

    users_collection.insert_many(users)

    return {"message": "100 users inserted"}

# This route finds all users under the age of 25 and returns their details.
@app.get("/users-under-25", tags=["Find"])
def users_under_25():
    users = list(users_collection.find({"age": {"$lt": 25}}))

    for user in users:
        user["_id"] = str(user["_id"])
        user["address_id"] = str(user["address_id"])

    return users
# This route finds all users over the age of 60 and returns their details.
@app.get("/users-over-60", tags=["Find"])
def users_over_60():
    users = list(users_collection.find({"age": {"$gt": 60}}))

    for user in users:
        user["_id"] = str(user["_id"])
        user["address_id"] = str(user["address_id"])

    return users

# This route sorts users by their age in ascending order and returns their details.
@app.get("/sort-users-by-age", tags=["Sort"])
def sort_users_by_age():
    users = list(users_collection.find().sort("age", 1))
    for user in users:
        user["_id"] = str(user["_id"])  
        user["address_id"] = str(user["address_id"])
    return users

# This route sorts users by their name in ascending order and returns their details.
@app.get("/sort-users-by-name", tags=["Sort"])
def sort_users_by_name():
    users = list(users_collection.find().sort("name", 1))
    for user in users:  
        user["_id"] = str(user["_id"])  
        user["address_id"] = str(user["address_id"])
    return users



app.include_router(aggregation_route.router, prefix="/aggregation", tags=["Aggregation"])