from fastapi import APIRouter, Body
from loguru import logger
from app.common.utils import transform_mongo_document
from app.controller.achievement import create_achievement
from app.schema.achievement import (AchievementSchema, AchievementResponse, CreateAchievementSchema)
from app.schema.base import build_response
router = APIRouter(
    prefix="/achievement",
    tags=["achievement"]
)
@router.post(path="/create",
             description="Create a new achievement",
             response_model=AchievementResponse)
async def create_achievement_route(achievement: CreateAchievementSchema = Body(...)):
    try:
        achievement_dict = achievement.model_dump()
        _id = await create_achievement(achievement_dict)
        if not id:
            return build_response(success=False, error="An error ocurred when creating the new achievement.", status_code=500)
        achievement_dict["_id"] = _id
        achievement_schema = AchievementSchema(**transform_mongo_document(achievement_dict))
        return build_response(success=True, data=achievement_schema, status_code=201)
    except Exception as e:
        logger.exception("Error occurred while creating achievement")
        return build_response(success=False, error="Failed to create achievement. Please try again later.", status_code=500)