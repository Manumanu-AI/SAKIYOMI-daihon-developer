from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timezone, timedelta

class InstagramTrendPost(BaseModel):
    post_id: Optional[str] = Field(None)
    image_url: str = Field(..., min_length=1, max_length=1000)
    caption: Optional[str] = Field(None, max_length=2000)
    likes_count: Optional[int] = Field(None, ge=0)
    comments_count: Optional[int] = Field(None, ge=0)
    created_at: datetime = Field(...)

    @validator('created_at', pre=True, always=True)
    def set_created_at(cls, v):
        if v is None:
            tokyo_tz = timezone(timedelta(hours=9))
            return datetime.now(tokyo_tz)
        return v

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 1000
        use_enum_values = True
        validate_assignment = True
