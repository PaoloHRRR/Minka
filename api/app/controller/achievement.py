from app.common.database import database
from app.schema.achievement import AchievementSchema
from bson.objectid import ObjectId
async def create_achievement(achievement_data: dict):
    achievement_data["image"] = ObjectId(achievement_data["image"])
    result = await database.Achievements.insert_one(achievement_data)
    return str(result.inserted_id)