from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

from app.schema.base import BodySchema, ResponseSchema
from app.common.constants import NOW


class DonationSchema(BaseModel):
    donor: str = Field(..., min_length=1, description="Reference to the donor, linking to the Donors collection")
    project: str = Field(..., min_length=1, description="Reference to the project, linking to the Projects collection")
    donation_date: datetime = Field(None, description="Date of the donation")
    type: str = Field(..., description="Type of donation.", enum=["monetary", "in-kind", "service"])
    donation_amount: int = Field(...,gt=0,description="Amount of the donation")

    def __init__(self, **data):
        super().__init__(**data)
        self.donation_date = NOW()


class DonationBody(BodySchema):
    data: DonationSchema


class DonationResponse(ResponseSchema):
    body: DonationBody


""" FETCH
"""

class FetchDonationsSchema(BaseModel):
    donations: List[DonationSchema]
    total: int


class FetchDonationsBody(BodySchema):
    data: FetchDonationsSchema


class FetchDonationsResponse(ResponseSchema):
    body: FetchDonationsBody