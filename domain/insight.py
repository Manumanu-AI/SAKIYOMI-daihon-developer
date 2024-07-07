# domain/insight.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Insight(BaseModel):
    post_id: str = Field(..., description="Unique identifier for the post")
    caption: str = Field(..., description="Caption of the post")
    comments_count: int = Field(..., ge=0, description="Number of comments")
    likes_count: int = Field(..., ge=0, description="Number of likes")
    video_view_count: Optional[int] = Field(None, ge=0, description="Number of video views")
    timestamp: datetime = Field(..., description="Timestamp of the post")
    type: str = Field(..., description="Type of the post")
    user_id: str = Field(..., description="ID of the user who posted")

    class Config:
        allow_population_by_field_name = True
