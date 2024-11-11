from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from app.common.constants import Env
client = AsyncIOMotorClient("mongodb://MinkaADMIN:m1nk44dm1n@mongodb:27017/")
database = client["Minka"]