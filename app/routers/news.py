from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Literal
from ..mongo import MongoClient
from ..config import MongoConfig
from bson import ObjectId

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.get("/get_news_simple")
async def get_news_simple(
    last_retrieved_id: Optional[str] = Query(None, description="Last retrieved document ID"),
    navigation: Optional[Literal["next", "previous"]] = Query("next", description="Navigation direction"),
    category: Optional[str] = Query(None, description="Category to filter news items")
):
    """
    Get news articles with navigation support and category filtering.
    
    Args:
        last_retrieved_id: ID of the last retrieved document
        navigation: Direction of navigation ('next' for older news, 'previous' for newer news)
        category: Optional category to filter news items
    
    Returns:
        Latest news item if no last_retrieved_id is provided,
        Next older item if navigation is 'next',
        Next newer item if navigation is 'previous'
        Filtered by category if specified
    """
    print(f"Payload: {last_retrieved_id}, {navigation}, {category}")
    try:
        # Build the query based on last_retrieved_id, navigation and category
        query = {}
        sort_order = -1  # Default descending order for latest first
        
        # Add category filter if provided
        if category:
            query["category"] = category
        
        if last_retrieved_id:
            try:
                last_id = ObjectId(last_retrieved_id)
                if navigation == "next":
                    # Get older news (smaller ObjectId)
                    query["_id"] = {"$lt": last_id}
                    sort_order = -1
                else:  # navigation == "previous"
                    # Get newer news (larger ObjectId)
                    query["_id"] = {"$gt": last_id}
                    sort_order = 1
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid ObjectId format: {str(e)}")

        # Fetch current document
        news_items = MongoClient.search_collection(
            database=MongoConfig.NEWS_DATABASE,
            collection=MongoConfig.NEWS_COLLECTION,
            query=query,
            sort=[("_id", sort_order)],
            limit=1
        )
        
        if not news_items:
            return {
                "message": "No more news items available",
                "id": None,
                "data": None,
                "has_next": False,
                "has_previous": False
            }
        
        # Get the first (and only) item
        news_item = news_items[0]
        
        # Convert ObjectId to string for JSON serialization
        news_id = str(news_item["_id"])
        news_item["_id"] = news_id
        
        # Check if there are more items in either direction
        next_query = {"_id": {"$lt": ObjectId(news_id)}}
        previous_query = {"_id": {"$gt": ObjectId(news_id)}}
        
        # Add category filter to next/previous queries if category is specified
        if category:
            next_query["category"] = category
            previous_query["category"] = category
        
        next_items = MongoClient.search_collection(
            database=MongoConfig.NEWS_DATABASE,
            collection=MongoConfig.NEWS_COLLECTION,
            query=next_query,
            sort=[("_id", -1)],
            limit=1
        )
        
        previous_items = MongoClient.search_collection(
            database=MongoConfig.NEWS_DATABASE,
            collection=MongoConfig.NEWS_COLLECTION,
            query=previous_query,
            sort=[("_id", 1)],
            limit=1
        )
        print("Current id: ", news_id)

        # The "description" field has <p> tags, so we need to remove them
        news_item["description"] = (
            news_item["description"].replace("<p>", "").replace("</p>", "")
            if news_item["description"] is not None
            else ""
        )

        return {
            "message": "Success",
            "id": news_id,
            "data": news_item,
            "has_next": len(next_items) > 0,
            "has_previous": len(previous_items) > 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
