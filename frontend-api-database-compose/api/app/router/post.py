from datetime import datetime
from fastapi import APIRouter, Body
from loguru import logger
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from app.schema.post import *
from app.controller.post import *

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

@router.get(path="/all",
            description="Fetch all posts",
            response_model=FetchPostsResponse)
async def fetch_posts():
    try:
        posts = await fetch_all_posts()
        post_schemas = [PostSchema(**post) for post in posts]
        fetch_posts_schema = FetchPostsSchema(posts=post_schemas, total=len(post_schemas))
        return build_response(success=True, data=fetch_posts_schema, status_code=200)
    except Exception:
        logger.exception("fetch_posts")
        return build_response(success=False, error="An error occurred while fetching posts", status_code=500)

# ya no se usa
@router.get(path="/{post_id}",
            description="Get a post by id",
            response_model=PostResponse)
async def get_post(post_id: str):
    try:
        post = await fetch_post_by_id(post_id)
        if not post:
            return build_response(success=False, error="No records found", status_code=404)
        post_schema = PostSchema(**transform_mongo_document(post))
        return build_response(success=True, data=post_schema, status_code=200)
    except Exception:
        logger.exception("get_post")
        return build_response(success=False, error="An error occurred while fetching this post", status_code=500)

@router.get(
    path="/by-ngod-name/{ngod_name}",
    description="Get all posts by NGOD name",
    response_model=List[PostResponse]
)
async def get_posts_by_ngod_name(ngod_name: str):
    try:
        ngod = await database.NGODs.find_one({"name": ngod_name})
        if not ngod:
            return build_response(success=False, error="ONG not found", status_code=404)
        ngod_id = ngod["_id"]
        posts = await database.Posts.find({"publisher": ObjectId(ngod_id)}).to_list(length=None)
        if not posts:
            return build_response(success=False, error="No posts found for this NGOD", status_code=404)
        post_schemas = [PostSchema(**transform_mongo_document(post)) for post in posts]
        return build_response(success=True, data=post_schemas, status_code=200)
    except Exception:
        logger.exception("get_posts_by_ngod_name")
        return build_response(success=False, error="An error occurred while fetching posts for this NGOD", status_code=500)
    
@router.post(path="/new",
             description="Create a new post",
             response_model=PostResponse)
async def create(post: RegisterPostSchema = Body(...)):
    try:
        post_dict = post.model_dump()
        post_dict["comments"] = []
        id = await create_post(post_dict)
        if not id:
            return build_response(success=False, error="An error occurred while uploading the new post", status_code=500)
        
        post_schema = PostSchema(**transform_mongo_document(post_dict))
        return build_response(success=True, data=post_schema, status_code=200)
    except Exception:
        logger.exception("create_post")
        return build_response(success=False, error="An error occurred while creating a new post", status_code=500)
    
@router.post(path="/{post_id}/comment",
             description="Add a comment to a post",
             response_model=PostResponse)
async def add_comment(post_id: str, comment: CommentSchema = Body(...)):
    try:
        comment_dict = comment.model_dump()
        success = await add_comment_to_post(post_id, comment_dict)
        if not success:
            return build_response(success=False, error="Post not found or comment not added", status_code=404)
        return build_response(success=True, data="Comment added successfully", status_code=201)
    except Exception:
        logger.exception("add_comment")
        return build_response(success=False, error="An error occurred while adding the comment", status_code=500)
