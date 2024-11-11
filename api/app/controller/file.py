from app.common.database import database
from bson import Binary, ObjectId
from typing import Optional
async def save_file(file_data: dict):
    file_data["file_data"] = Binary(file_data["file_data"])
    result = await database.Files.insert_one(file_data)
    return result.inserted_id
async def take_file(file_id: str) -> Optional[dict]: 
    if not ObjectId.is_valid(file_id):
        return None
    result = await database.Files.find_one({"_id": ObjectId(file_id)})
    return result