from typing import Optional
from app.common.database import database
from app.common.utils import transform_mongo_document
import re
async def fetch_all_ngods():
    ngods = await database.NGODs.find().to_list(1000)
    return [transform_mongo_document(ngod) for ngod in ngods]
async def fetch_ngod_by_name(ngod_name: str) -> Optional[dict]:
    ngod = await database.NGODs.find_one({"name": ngod_name})
    return ngod["_id"]
async def fetch_ngods_by_partial_name(ngod_name: str):
    pattern = re.compile(ngod_name, re.IGNORECASE)
    ngods = await database.NGODs.find({"name": {"$regex": pattern}}).to_list(1000)
    return [transform_mongo_document(ngod) for ngod in ngods]