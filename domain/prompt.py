from pydantic import BaseModel, Field, validator, model_validator

class Prompt(BaseModel):
    prompt_id: str = Field(..., min_length=1, max_length=100)
    user_id: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    text: str = Field(..., min_length=1, max_length=10000)

    @validator('type')
    def validate_type(cls, v):
        allowed_types = ['post', 'title']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of {allowed_types}')
        return v

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 1000
        use_enum_values = True
        validate_assignment = True
