from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class CanvaTemplate(BaseModel):
    id: str = Field(..., min_length=1, max_length=100)
    button_url: HttpUrl
    embed_url: HttpUrl
    name: str = Field(..., min_length=1, max_length=100)

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 100
        use_enum_values = True
        validate_assignment = True