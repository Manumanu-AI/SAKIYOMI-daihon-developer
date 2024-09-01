# domain/performance.py
from typing import Optional
from pydantic import BaseModel, Field

class Performance(BaseModel):
    feed_run: Optional[int] = Field(0, ge=0)
    reel_run: Optional[int] = Field(0, ge=0)
    feed_theme_run: Optional[int] = Field(0, ge=0)
    reel_theme_run: Optional[int] = Field(0, ge=0)
    data_analysis_run: Optional[int] = Field(0, ge=0)

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
