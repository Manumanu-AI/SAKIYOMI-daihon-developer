from typing import Optional
from pydantic import BaseModel, Field, validator, model_validator


class Prompt(BaseModel):
    prompt_id: str = Field(..., min_length=1, max_length=100)
    user_id: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    text: str = Field(..., min_length=1, max_length=10000)
    example_plot: Optional[str] = Field(None, min_length=1, max_length=10000)

    @validator('type')
    def validate_type(cls, v):
        allowed_types = ['feed_post', 'feed_theme', 'reel_post', 'reel_theme', 'insight_analysis']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of {allowed_types}')
        return v

    @model_validator(mode='before')
    def check_example_plot(cls, values):
        text = values.get('text')
        example_plot = values.get('example_plot')

        if '{example_plot}' in text and example_plot is None:
            raise ValueError('example_plot must not be None if text contains {example_plot}')

        return values

    def embed_example_plot(self):
        if '{example_plot}' in self.text:
            self.text = self.text.replace("{example_plot}", self.example_plot or "")

    class Config:
        str_strip_whitespace = True
        str_min_length = 1
        str_max_length = 1000
        use_enum_values = True
        validate_assignment = True
