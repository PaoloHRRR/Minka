from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

from app.schema.base import BodySchema, ResponseSchema
from app.common.security import hash_password
from app.common.constants import NOW


"""  NGOD SCHEMAS
"""

class AddressSchema(BaseModel):
    streetAddress: str = Field(...,description="The street address where the NGO is physically located")
    department: str = Field(..., description="The main administrative division, often equivalent to a state, where the NGO is located")
    province: str = Field(...,description="The province or secondary administrative region within the department")
    district: str = Field(...,description="The specific district or local administrative area of the NGO")

class ContactSchema(BaseModel):
    email: EmailStr = Field(default_factory=lambda: "", description="NOGD's email address, must be a valid email format")
    phone: str = Field(default_factory=lambda: "", description="Contact phone number of the NGO, must be a valid phone number")

class SocialMediaSchema(BaseModel):
    name: str = Field(default_factory=lambda: "",description="Name of the social media platform")
    link: str = Field(default_factory=lambda: "",description="URL link to the NGO\'s social media profile")

class NGODSchema(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str = Field(..., min_length=1, description="NGOD's name")
    profile_picture: Optional[str] = Field(default_factory=lambda: "", description="Profile picture of the NGOD")
    status: str = Field(..., description="NGOD status", enum=["active","inactive","pending"])
    description: str = Field(...,description="Description of the NGOD")
    registration_date: Optional[datetime] = Field(default_factory=lambda: NOW(), description="NGOD's registration date on the platform")
    legal_documents: Optional[List[str]] = Field(default_factory=lambda: [], description="NGOD's legal documents")
    projects: Optional[List[str]] = Field(default_factory=lambda: [], description="NGOD's projects")
    address: AddressSchema = Field(...,description="Address of the NGOD")
    contact: Optional[ContactSchema] = Field(default_factory=lambda: [],description="Contact information for the NGO")
    social_media: Optional[SocialMediaSchema] = Field(default_factory=lambda: [],description="Social media accounts of the NGO")

class NGODBody(BodySchema):
    data: NGODSchema


class NGODResponse(ResponseSchema):
    body: NGODBody

""" FETCH ALL
"""


class FetchNGODsSchema(BaseModel):
    ngods: List[NGODSchema]
    total: int
    page: int
    total_pages: int


class FetchNGODsBody(BodySchema):
    data: FetchNGODsSchema


class FetchNGODsResponse(ResponseSchema):
    body: FetchNGODsBody

