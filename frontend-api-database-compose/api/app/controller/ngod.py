from bson.objectid import ObjectId
from typing import Optional
from app.common.database import database
from app.common.utils import transform_mongo_document
import re


async def fetch_all_ngods():
    ngods = await database.NGODs.find().to_list(50)
    return [transform_mongo_document(ngod) for ngod in ngods]

async def fetch_ngod_by_name(ngod_name: str) -> Optional[dict]:
    ngod = await database.NGODs.find_one({"name": ngod_name})
    return ngod

async def fetch_ngods_by_partial_name(ngod_name: str):
    pattern = re.compile(ngod_name, re.IGNORECASE)
    ngods = await database.NGODs.find({"name": {"$regex": pattern}}).to_list(1000)
    return [transform_mongo_document(ngod) for ngod in ngods]

async def get_ngod_name(ngod_id: str) -> Optional[str]:
    ngod = await database.NGODs.find_one({"_id": ObjectId(ngod_id)})
    return ngod["name"]

async def fetch_paginated_ngods(page: int, limit: int):
    skip = (page - 1) * limit
    ngods = await database.NGODs.find().skip(skip).limit(limit).to_list(limit)
    return [transform_mongo_document(ngod) for ngod in ngods]

async def fetch_paginated_ngods_by_partial_name(ngod_name: str, page: int, limit: int):
    skip = (page - 1) * limit
    
    query = {"name": {"$regex": ngod_name, "$options": "i"}}
    
    ngods_cursor = database.NGODs.find(query).skip(skip).limit(limit)
    ngods = await ngods_cursor.to_list(length=limit)
    
    total_count = await database.NGODs.count_documents(query)
    
    return [transform_mongo_document(ngod) for ngod in ngods], total_count