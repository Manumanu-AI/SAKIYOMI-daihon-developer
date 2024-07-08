# domain/insight.py

from pydantic import BaseModel, Field
from datetime import datetime
import random
import string

def generate_post_id():
    return ''.join(random.choices(string.digits, k=10))

class Insight(BaseModel):
    post_id: str = Field(default_factory=generate_post_id)
    user_id: str
    created_at: datetime
    posted_at: datetime  # 新しく追加
    post_url: str  # first_viewをpost_urlに変更
    followers_reach_count: int
    like_count: int
    new_reach_count: int
    plot: str
    reach_count: int
    save_count: int

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_dict(cls, data: dict):
        if 'created_at' in data and isinstance(data['created_at'], (int, float)):
            data['created_at'] = datetime.fromtimestamp(data['created_at'])
        if 'posted_at' in data and isinstance(data['posted_at'], (int, float)):
            data['posted_at'] = datetime.fromtimestamp(data['posted_at'])
        return cls(**data)
