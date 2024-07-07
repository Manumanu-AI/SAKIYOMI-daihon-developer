# domain/insight.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Insight(BaseModel):
    post_id: str = Field(..., description="Unique identifier for the post")
    created_at: datetime = Field(..., description="Creation timestamp of the post")
    first_view: str = Field(..., description="First view source")
    followers_reach_count: int = Field(..., description="Number of followers reached")
    like_count: int = Field(..., description="Number of likes")
    new_reach_count: int = Field(..., description="Number of new reaches")
    plot: Optional[str] = Field(None, description="Plot data")
    reach_count: str = Field(..., description="Total reach count")
    save_count: int = Field(..., description="Number of saves")

    class Config:
        allow_population_by_field_name = True
