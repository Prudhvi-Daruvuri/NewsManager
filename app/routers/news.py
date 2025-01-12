from fastapi import APIRouter, HTTPException
from typing import List, Optional
from .. import schemas
from ..mongo import MongoClient
from ..config import MongoConfig
from bson import ObjectId

from fastapi import Query

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.get("/get_news_simple")
async def get_news_simple(last_retrieved_id: Optional[str] = Query(None, description="Last retrieved document ID")):
    """
    Get news articles after the last retrieved ID, sorted by creation date in descending order.
    If no last_retrieved_id is provided, returns the latest document.
    """
    try:
        print(f"last_retrieved_id: {last_retrieved_id}")
        # Build the query based on last_retrieved_id
        query = {}
        if last_retrieved_id:
            try:
                # Convert last_retrieved_id to ObjectId
                last_id = ObjectId(last_retrieved_id)
                # Get documents with _id less than the last retrieved id
                query = {"_id": {"$lt": last_id}}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid ObjectId format: {str(e)}")

        # Fetch documents
        result = MongoClient.search_collection(
            database=MongoConfig.NEWS_DATABASE,
            collection=MongoConfig.NEWS_COLLECTION,
            query=query,
            sort=[("_id", -1)],  # Descending order
            limit=1
        )
        
        # Check if the result is already a list
        if isinstance(result, list):
            news_items = result
        else:
            # Convert cursor to list if it's not already a list
            news_items = await result.to_list(length=1)

        if not news_items:
            return {"message": "No more news items available", "id": None, "data": None}
        
        # Get the first (and only) item
        news_item = news_items[0]
        
        # Convert ObjectId to string for JSON serialization
        news_id = str(news_item["_id"])
        news_item["_id"] = news_id
        
        return news_item

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")