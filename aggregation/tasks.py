from fastapi import APIRouter
from database import orders_collection
from datetime import datetime, timedelta

router = APIRouter()

# Task 1: Daily sales total and order count
@router.get("/daily-sales")
def daily_sales(
    date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):

    if date:
        start = datetime.fromisoformat(date)
        end = start + timedelta(days=1)
    else:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date) + timedelta(days=1)

    pipeline = [

        # Convert string order_date → Mongo Date
        {
            "$addFields": {
                "order_date_obj": {
                    "$toDate": "$order_date"
                }
            }
        },

        # Filter by date range
        {
            "$match": {
                "order_date_obj": {
                    "$gte": start,
                    "$lt": end
                }
            }
        },

        # Group by day
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$order_date_obj"
                    }
                },
                "total_sales": {"$sum": "$total_amount"},
                "orders_count": {"$sum": 1}
            }
        },

        # Sort by date
        {
            "$sort": {"_id": 1}
        }
    ]

    sales = list(orders_collection.aggregate(pipeline))

    format_sales = []
    for item in sales:
        format_sales.append({
            "Date": item["_id"],
            "Total Sales": round(item["total_sales"], 2),
            "Orders": item["orders_count"]
        })
    return format_sales

# Task 2: Top 5 customers by Spending
@router.get("/top-customers")
def top_customers(limit: int = 5):

    pipeline = [
        # group by customer
        {
            "$group": {
                "_id": "$customer_id",
                "total_spent": {"$sum": "$total_amount"},
                "orders": {"$sum": 1},
                "last_order": {"$max": "$order_date_obj"}
            }
        },

        # sort by highest spending
        {
            "$sort": {"total_spent": -1}
        },

        # top N customers
        {
            "$limit": limit
        },

        # format output
        {
            "$project": {
                "_id": 0,
                "Customer": "$_id",
                "Total Spent": {"$round": ["$total_spent", 2]},
                "Orders": "$orders",
                "Last Order": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$last_order"
                    }
                }
            }
        }
    ]

    result = list(orders_collection.aggregate(pipeline))
    return result

# Task 3: Sales by City(Top 20)
@router.get("/cities")
def sales_by_city(limit: int = 20):

    pipeline = [

        # group orders by city
        {
            "$group": {
                "_id": "$city",
                "total_sales": {"$sum": "$total_amount"},
                "orders": {"$sum": 1},
                "avg_order": {"$avg": "$total_amount"}
            }
        },

        # sort by highest total sales
        {
            "$sort": {"total_sales": -1}
        },

        # limit results
        {
            "$limit": limit
        },

        # format response
        {
            "$project": {
                "_id": 0,
                "City": "$_id",
                "Total Sales": {"$round": ["$total_sales", 2]},
                "Orders": "$orders",
                "Avg Order": {"$round": ["$avg_order", 2]}
            }
        }

    ]

    result = list(orders_collection.aggregate(pipeline))
    return result