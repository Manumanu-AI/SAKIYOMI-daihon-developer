from pydantic import BaseModel, Field, validator

class UserIndex(BaseModel):
    index_id: str = Field(..., min_length=1, max_length=100)
    user_id: str = Field(..., min_length=1, max_length=100)
    index_name: str = Field(..., min_length=1, max_length=100)
    langsmith_project_name: str = Field(..., min_length=1, max_length=100)
    pinecone_api_key: str = Field(..., min_length=1, max_length=1000)
    type: str = Field(..., min_length=1, max_length=50)

    @validator('index_name', 'langsmith_project_name')
    def validate_non_empty(cls, v):
        if not v:
            raise ValueError('This field cannot be empty')
        return v

    @validator('type')
    def validate_type(cls, v):
        allowed_types = ['feed', 'reel']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of {allowed_types}')
        return v

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 100
        use_enum_values = True
        validate_assignment = True
