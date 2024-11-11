from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schema.base import BodySchema, ResponseSchema
from app.common.constants import NOW
class AchievementSchema(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str = Field(..., min_length=1, description="Name of the achievement, cannot be empty")
    description: str = Field(..., min_length=1, description="Detailed description of the achievement")
    creation_date: Optional[datetime] = Field(default_factory=lambda: NOW(), description="Date when the achievement was created")
    image: str = Field(..., description="ObjectId reference to the achievement image")
class AchievementBody(BodySchema):
    data: AchievementSchema
class AchievementResponse(ResponseSchema):
    body: AchievementBody
''' CREATE
'''
class CreateAchievementSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the achievement, cannot be empty")
    description: str = Field(..., min_length=1, description="Detailed description of the achievement")
    creation_date: Optional[datetime] = Field(default_factory=lambda: NOW(), description="Date when the achievement was created")
    image: str = Field(..., description="ObjectId reference to the achievement image")