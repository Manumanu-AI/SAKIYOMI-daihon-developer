from pydantic import BaseModel, Field, validator

class UserIndex(BaseModel):
    index_id: str = Field(..., min_length=1, max_length=100)
    user_id: str = Field(..., min_length=1, max_length=100)
    index_name: str = Field(..., min_length=1, max_length=100)
    langsmith_project_name: str = Field(..., min_length=1, max_length=100)

    @validator('index_name', 'langsmith_project_name')
    def validate_non_empty(cls, v):
        if not v:
            raise ValueError('This field cannot be empty')
        return v

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 100
        use_enum_values = True
        validate_assignment = True
