from bson.objectid import ObjectId
from typing import Optional, List
from app.common.database import database
from app.common.utils import transform_mongo_document
async def fetch_all_posts():
    posts = await database.Posts.find().to_list(1000)
    return [transform_mongo_document(post) for post in posts]
async def fetch_post_by_id(post_id: str) -> Optional[dict]:
    if not ObjectId.is_valid(post_id):
        return None
    post = await database.Posts.find_one({"_id": ObjectId(post_id)})
    return post
async def fetch_posts_by_ngod_id(ngod_id: str) -> Optional[List[dict]]:
    if not ObjectId.is_valid(ngod_id):
        return None
    posts = await database.Posts.find({"ngod_id": ObjectId(ngod_id)}).to_list(length=None)
    return posts
async def create_post(post_data: dict):
    post_data["publisher"] = ObjectId(post_data["publisher"])
    if post_data["content"]["files"]:
        post_data["content"]["files"] = [ObjectId(file_id) for file_id in post_data["content"]["files"] if ObjectId.is_valid(file_id)]
    result = await database.Posts.insert_one(post_data)
    return result.inserted_id
async def add_comment_to_post(post_id: str, comment_data: dict) -> bool:
    if not ObjectId.is_valid(post_id):
        return False
    comment_data["user"] = ObjectId(comment_data["user"])
    if comment_data["content"]["files"]:
        comment_data["content"]["files"] = [ObjectId(file_id) for file_id in comment_data["content"]["files"] if ObjectId.is_valid(file_id)]
    result = await database.Posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment_data}}
    )
    return result.modified_count > 0