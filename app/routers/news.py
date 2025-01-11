from fastapi import APIRouter, HTTPException
from typing import List
from .. import schemas
from ..mongo import MongoDB

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.get("/", response_model=List[schemas.News])
async def read_news(skip: int = 0, limit: int = 100):
    news = await MongoDB.get_all_news(skip=skip, limit=limit)
    return news

@router.get("/{news_id}", response_model=schemas.News)
async def read_news_by_id(news_id: str):
    news = await MongoDB.get_news_by_id(news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.post("/", response_model=schemas.News)
async def create_news(news: schemas.NewsCreate):
    return await MongoDB.create_news(news)

@router.patch("/{news_id}", response_model=schemas.News)
async def update_news(news_id: str, news: schemas.NewsUpdate):
    updated_news = await MongoDB.update_news(news_id, news)
    if updated_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return updated_news

@router.delete("/{news_id}")
async def delete_news(news_id: str):
    success = await MongoDB.delete_news(news_id)
    if not success:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": "News deleted successfully"}
