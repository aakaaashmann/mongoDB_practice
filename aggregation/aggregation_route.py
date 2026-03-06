from fastapi import  APIRouter
from database import users_collection, address_collection

router = APIRouter()

# This route retrieves all users who live in a specific city
# performing a lookup to join the users collection with the addresses collection
# matching the city name, and returning the relevant user information along with their address details.
@router.get("/users?city={city}")
def users_by_city(city: str | None = None):
    pipeline = [
        {  
            "$lookup":{
                "from": "addresses",
                "localField": "address_id",
                "foreignField": "_id",
                "as": "address"
            }
        },
        {
            "$unwind": "$address"
        }
    ]
    if city:
        pipeline.append({
            "$match": {
                "address.city": city
            }
        })
    users = list(users_collection.aggregate(pipeline))
    for user in users:
        user["_id"] = str(user["_id"])  
        user["address_id"] = str(user["address_id"])
        user["address"]["_id"] = str(user["address"]["_id"])
    return users

# This route calculates the average age of users in each city 
# performing a lookup to join the users collection with the addresses collection
# grouping the results by city, and calculating the average age for each city.
@router.get("/users/average-age-by-city")
def average_age_by_city():
    pipeline = [
        {  
            "$lookup":{
                "from": "addresses",
                "localField": "address_id",
                "foreignField": "_id",
                "as": "address"
            }
        },
        {
            "$unwind": "$address"
        },
        {
            "$group": {
                "_id": "$address.city",
                "total_users":{"$sum":1},
                "average_age": {"$avg": "$age"}
            }
        }
    ]
    result = list(users_collection.aggregate(pipeline))
    for item in result:
        item["city"] = item.pop("_id")  
    return result

# This route groups users into age groups (Under 25, 25-60, Over 60)
# counts how many users fall into each age group.
@router.get("/users/age-groups")
def users_by_age_group():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "$cond": [
                        {"$lt": ["$age", 25]},
                        "Under 25",
                        {"$cond": [
                            {"$lt": ["$age", 60]},
                            "25-60",
                            "Over 60"
                        ]}
                    ]
                },
                "total_users": {"$sum": 1}
            }
        }
    ]
    result = list(users_collection.aggregate(pipeline))
    return result   

# This route combines both city and age group aggregation to provide 
# how many users fall into each age group for a specific city.
@router.get("/users?include=address")
def users_with_addresses():
    pipeline = [
        {  
            "$lookup":{
                "from": "addresses",
                "localField": "address_id",
                "foreignField": "_id",
                "as": "address"
            }
        },
        {
            "$unwind": "$address"
        }
    ]
    users = list(users_collection.aggregate(pipeline))
    for user in users:
        user["_id"] = str(user["_id"])  
        user["address_id"] = str(user["address_id"])
        user["address"]["_id"] = str(user["address"]["_id"])
    return users

# This route provides the count of users in each city 
# by performing a lookup to join the users collection with the addresses collection, grouping the results by city, and counting the number of users in each city.
@router.get("/users/count-by-city")
def user_count_by_city():
    pipeline = [
        {  
            "$lookup":{
                "from": "addresses",
                "localField": "address_id",
                "foreignField": "_id",
                "as": "address"
            }
        },
        {
            "$unwind": "$address"
        },
        {
            "$group": {
                "_id": "$address.city",
                "total_users":{"$sum":1}
            }
        }
    ]
    result = list(users_collection.aggregate(pipeline))
    for item in result:
        item["city"] = item.pop("_id")  
    return result

# This route combines both city and age group aggregation to provide 
# how many users fall into each age group for a specific city.
@router.get("/users/age-group?city={city_name}")
def city_by_age_group(city_name: str | None = None):
    pipeline = [
        {  
            "$lookup":{
                "from": "addresses",
                "localField": "address_id",
                "foreignField": "_id",
                "as": "address"
            }
        },
        {
            "$unwind": "$address"
        },
        {
            "$match": {
                "address.city" : city_name
            }
        },
        {
            "$group": {
                "_id": {
                    "$cond": [
                        {"$lt": ["$age", 25]},
                        "Under 25",
                        {"$cond": [
                            {"$lt": ["$age", 60]},
                            "25-60",
                            "Over 60"
                        ]}
                    ]
                },
                "total_users": {"$sum": 1}
            }
        }
    ]
    result = list(users_collection.aggregate(pipeline))
    for item in result:
        item["age_group"] = item.pop("_id")  
    return result
    