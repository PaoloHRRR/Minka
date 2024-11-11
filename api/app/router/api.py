from fastapi import APIRouter
from app.router.user import router as user
from app.router.post import router as post
from app.router.achievement import router as achievement
from app.router.donation import router as donation
from app.router.ngod import router as ngod
from app.router.file import router as file
api_router = APIRouter(
    prefix="/api",
    responses={
        404: {"description": "Not found"},
        408: {"description": "Timeout"}
        }
    )
api_router.include_router(user)
api_router.include_router(post)
api_router.include_router(achievement)
api_router.include_router(donation)
api_router.include_router(ngod)
api_router.include_router(file)