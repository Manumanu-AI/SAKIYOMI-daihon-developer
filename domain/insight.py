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
    reach_count: int = Field(..., description="Total reach count")
    save_count: int = Field(..., description="Number of saves")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.timestamp()  # datetime をタイムスタンプに変換
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Firestoreのタイムスタンプをdatetimeに変換
        if 'created_at' in data and isinstance(data['created_at'], (int, float)):
            data['created_at'] = datetime.fromtimestamp(data['created_at'])
        
        # reach_countを文字列から整数に変換
        if 'reach_count' in data and isinstance(data['reach_count'], str):
            data['reach_count'] = int(data['reach_count'])
        
        return cls(**data)
