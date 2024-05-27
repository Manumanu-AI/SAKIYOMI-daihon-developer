from pydantic import BaseModel, Field, validator, root_validator, EmailStr
from typing import Optional, Any
from datetime import datetime
from firebase_admin import firestore
from type.custom_types import FirestoreServerTimestamp, is_firestore_server_timestamp

class User(BaseModel):
    user_id: str = None
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=50)
    created_at: Optional[Any] = Field(None)
    instagram_username: str = Field(..., min_length=1, max_length=100)

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['user', 'admin']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of {allowed_roles}')
        return v

    @root_validator(pre=True)
    def set_created_at(cls, values):
        if 'created_at' not in values or values['created_at'] is None:
            values['created_at'] = firestore.SERVER_TIMESTAMP
        return values

    @validator('created_at')
    def validate_created_at(cls, v):
        if not is_firestore_server_timestamp(v) and not isinstance(v, datetime):
            raise ValueError('created_at must be a Firestore server timestamp or a datetime object')
        return v

    @validator('instagram_username')
    def validate_instagram_username(cls, v):
        if not v.startswith('@'):
            raise ValueError('Instagram username must start with "@"')
        return v

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 1000
        use_enum_values = True
        validate_assignment = True
