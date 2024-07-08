# domain/insight.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import random
import string

def generate_post_id():
    return ''.join(random.choices(string.digits, k=10))

class Insight(BaseModel):
    post_id: str = Field(default_factory=generate_post_id)
    user_id: str
    created_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None
    post_url: Optional[str] = Field(None, alias='first_view')
    followers_reach_count: Optional[int] = None
    like_count: Optional[int] = None
    new_reach_count: Optional[int] = None
    plot: Optional[str] = None
    reach_count: Optional[int] = None
    save_count: Optional[int] = None
    example_plot: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, data: dict):
        for field in ['created_at', 'posted_at']:
            if field in data and isinstance(data[field], (int, float)):
                data[field] = datetime.fromtimestamp(data[field])
        return cls(**{k: v for k, v in data.items() if k in cls.__fields__})
