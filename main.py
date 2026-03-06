from fastapi import FastAPI, Query
from database import orders_collection
from bson import ObjectId
import random
from aggregation import aggregation_route , tasks

app = FastAPI( 
    title="FastAPI + MongoDB",
    description="A simple FastAPI application demonstrating MongoDB integration with aggregation pipelines.",
    version="1.0.0",
)


app.include_router(tasks.router)



# @app.get("/", tags=["Root"])
# def home():
#     return {"message": "FastAPI + MongoDB Working 🚀"}


# @app.post("/create-addresses", tags=["Create"])
# def create_addresses():
#     cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
#               "Hyderabad", "Pune", "Allahabad", "Varanasi", "Lucknow"
#     ]

#     data = [{"city": city} for city in cities]
#     address_collection.insert_many(data)

#     return {"message": "Addresses inserted"}

# @app.post("/insert-users", tags=["Create"])
# def insert_users():
#     addresses = list(address_collection.find())

#     users = []

#     for i in range(100):
#         user = {
#             "name": f"User{i}",
#             "age": random.randint(15,75),
#             "address_id": random.choice(addresses)["_id"]
#         }
#         users.append(user)

#     users_collection.insert_many(users)

#     return {"message": "100 users inserted"}

# # This route finds all users under the age of 25 and returns their details.

# @app.get("/users", tags=["Read"])
# def get_users(
#     age_lt: int | None = None,
#     age_gt: int | None = None,
#     sort: str | None = None
# ):
#     query = {}

#     if age_lt:
#         query["age"] = {"$lt": age_lt}
#     if age_gt:
#         query["age"] = {"$gt": age_gt}
#     users = list(users_collection.find(query))
#     for user in users:
#         user["_id"] = str(user["_id"])
#         if "address_id" in user:
#             user["address_id"] = str(user["address_id"])
#     return users


# app.include_router(aggregation_route.router, prefix="/agg", tags=["Aggregation"])

