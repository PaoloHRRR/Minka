from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from app.common.constants import Env

client = AsyncIOMotorClient("mongodb://admin:admin123@mongodb:27017/")
database = client["Minka"]

