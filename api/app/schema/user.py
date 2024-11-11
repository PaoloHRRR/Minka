from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from app.schema.base import BodySchema, ResponseSchema
from app.common.security import hash_password
from app.common.constants import NOW
"""  USER SCHEMAS
"""
class StatsSchema(BaseModel):
    number_of_posts: int = Field(default_factory=lambda: 0, description="Total number of posts made by the user")
    number_of_donations: int = Field(default_factory=lambda: 0, description="Total number of donations made by the user")
    total_donations: float = Field(default_factory=lambda: 0, description="Total monetary value of donations made by the user")
    days_as_good_person: int = Field(default_factory=lambda: 0, description="Total days the user has maintained a good standing")
class UserSchema(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str = Field(..., min_length=1, description="User's full name, cannot be empty")
    password: str = Field(..., min_length=1, description="User's safe password after hashing")
    email: EmailStr = Field(..., description="User's email address, must be a valid email format")
    system_role: str = Field(..., description="User's role within the system", enum=["admin", "user"])
    registration_date: datetime = Field(default_factory=lambda: NOW(), description="User registration date")
    achievements: Optional[List[StatsSchema]] = Field(None, description="User's achievements")
class UserBody(BodySchema):
    data: UserSchema
class UserResponse(ResponseSchema):
    body: UserBody
""" REGISTER
"""
class RegisterSchema(BaseModel):
    name: str = Field(..., min_length=1, description="User's full name, cannot be empty")
    password: str = Field(..., min_length=1, description="User's safe password after hashing")
    email: EmailStr = Field(..., description="User's email address, must be a valid email format")
    system_role: str = Field(default_factory=lambda:"user", description="User's role within the system", enum=["admin", "user"])
    registration_date: Optional[datetime] = Field(default_factory=lambda: NOW(), description="User registration date")
    def __init__(self, **data):
        super().__init__(**data)
        self.password = hash_password(self.password)
""" FETCH ALL
"""
class FetchUsersSchema(BaseModel):
    users: List[UserSchema]
    total: int
class FetchUsersBody(BodySchema):
    data: FetchUsersSchema
class FetchUsersResponse(ResponseSchema):
    body: FetchUsersBody
''' LOGIN
'''
class LoginSchema(BaseModel):
    email: str
    password: str
class TokenSchema(BaseModel):
    access_token: str
class TokenBody(BodySchema):
    data: TokenSchema
class TokenResponse(ResponseSchema):
    body: TokenBody