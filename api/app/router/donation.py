from fastapi import APIRouter, Body
from loguru import logger
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from app.schema.donation import (DonationSchema, DonationResponse,
                                 MakeDonationSchema,
                                FetchDonationsSchema, FetchDonationsResponse)
from app.controller.donation import (create_donation,
                                     fetch_donations_by_donor, fetch_donations_by_project)
router = APIRouter(
    prefix="/donation",
    tags=["donation"]
)
@router.post(path="/make",
             description="Register a new donation",
             response_model=DonationResponse)
async def register_donation(donation: MakeDonationSchema = Body(...)):
    try:
        donation_dict = donation.model_dump()
        _id = await create_donation(donation_dict)
        donation_dict["_id"] = _id
        donation_schema = DonationSchema(**transform_mongo_document(donation_dict))
        if donation_schema:
            return build_response(success=True, data=donation_schema, status_code=200)
    except Exception:
        logger.exception("Error occurred while registering donation")
        return build_response(success=False, error="Failed to register donation. Please try again later.", status_code=500)
@router.get(path="/by-donor/{donor_id}",
            description="Fetch donations by donor",
            response_model=FetchDonationsResponse)
async def fetch_donations_by_donor_route(donor_id: str):
    try:
        donations = await fetch_donations_by_donor(donor_id)
        donation_schemas = []
        for donation in donations:
            donation["donor"] = str(donation["donor"])
            donation["project"] = str(donation["project"])
        donation_schemas = [
            DonationSchema(**transform_mongo_document(donation)) for donation in donations
        ]
        fetch_donations_schema = FetchDonationsSchema(donations=donation_schemas, total=len(donation_schemas))
        return build_response(success=True, data=fetch_donations_schema, status_code=200)
    except Exception:
        logger.exception("Error occurred while fetching donations by donor")
        return build_response(success=False, error="Failed to fetch donations by donor. Please try again later.", status_code=500)
@router.get(path="/by-project/{project_id}",
            description="Fetch donations by project",
            response_model=FetchDonationsResponse)
async def fetch_donations_by_project_route(project_id: str):
    try:
        donations = await fetch_donations_by_project(project_id)
        donation_schemas = []
        for donation in donations:
            donation["donor"] = str(donation["donor"])
            donation["project"] = str(donation["project"])
        donation_schemas = [
            DonationSchema(**transform_mongo_document(donation)) for donation in donations
        ]
        fetch_donations_schema = FetchDonationsSchema(donations=donation_schemas, total=len(donation_schemas))
        return build_response(success=True, data=fetch_donations_schema, status_code=200)
    except Exception:
        logger.exception("Error occurred while fetching donations by project")
        return build_response(success=False, error="Failed to fetch donations for the project. Please try again later.", status_code=500)