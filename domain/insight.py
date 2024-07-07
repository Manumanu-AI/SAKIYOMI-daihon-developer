# domain/insight.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any

class Insight(BaseModel):
    post_id: Optional[str] = None
    created_at: Optional[datetime] = None
    first_view: Optional[str] = None
    followers_reach_count: Optional[int] = None
    like_count: Optional[int] = None
    new_reach_count: Optional[int] = None
    plot: Optional[str] = None
    reach_count: Optional[Any] = None  # Any型を使用して柔軟に対応
    save_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        if 'created_at' in data and isinstance(data['created_at'], (int, float)):
            data['created_at'] = datetime.fromtimestamp(data['created_at'])
        return cls(**data)
