from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NewsBase(BaseModel):
    title: str
    content: str
    author: str

class NewsCreate(NewsBase):
    pass

class News(NewsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
