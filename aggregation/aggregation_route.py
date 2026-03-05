from fastapi import  APIRouter
from database import users_collection, address_collection

router = APIRouter()


@router.get("/users-by-city/{city_name}")
def users_by_city(city_name: str):
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
        }
    ]
    users = list(users_collection.aggregate(pipeline))
    for user in users:
        user["_id"] = str(user["_id"])  
        user["address_id"] = str(user["address_id"])
        user["address"]["_id"] = str(user["address"]["_id"])
    return users

@router.get("/average-age-by-city")
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

@router.get("/users-by-age-group")
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

@router.get("/users-with-addresses")
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

@router.get("/user-count-by-city")
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

@router.get("/city-by-age-group")
def city_by_age_group(city_name: str):
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
    