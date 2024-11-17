from bson.objectid import ObjectId
from typing import Optional
from app.common.database import database

async def fetch_all_users():
    users = await database.Users.find().to_list(1000)
    return users

async def fetch_user_by_id(user_id: str):
    user = await database.Users.find_one({"_id": ObjectId(user_id)})
    return user

async def fetch_user_by_email(user_email: str):
    user = await database.Users.find_one({"email": user_email})
    return user

async def create_user(user_data: dict):
    result = await database.Users.insert_one(user_data)
    return result.inserted_id

async def get_user_name(ngod_id: str) -> Optional[str]:
    user = await database.Users.find_one({"_id": ObjectId(ngod_id)})
    return user["name"]