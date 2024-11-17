from app.common.database import database
from app.schema.donation import DonationSchema
from bson.objectid import ObjectId

async def create_donation(donation_data: dict):
    donation_data["donor"] = ObjectId(donation_data["donor"])
    donation_data["project"] = ObjectId(donation_data["project"])
    result = await database.Donations.insert_one(donation_data)
    return result.inserted_id

async def fetch_donations_by_donor(donor_id: str):
    donations = await database.Donations.find({"donor": ObjectId(donor_id)}).to_list(1000)
    return donations

async def fetch_donations_by_project(project_id: str):
    donations = await database.Donations.find({"project": ObjectId(project_id)}).to_list(1000)
    return donations