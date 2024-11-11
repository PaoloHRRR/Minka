from datetime import datetime
from fastapi import APIRouter, Body
from loguru import logger
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from app.schema.ngod import *
from app.controller.ngod import *
router = APIRouter(
    prefix="/ngod",
    tags=["ngod"]
)
@router.get(path="/all",
            description="Fetch all ngod",
            response_model=FetchNGODsResponse)
async def fetch_ngods():
    try:
        ngods = await fetch_all_ngods()
        ngod_schemas = [NGODSchema(**ngod) for ngod in ngods]
        fetch_ngods_schema = FetchNGODsSchema(ngods=ngod_schemas, total=len(ngod_schemas))
        return build_response(success=True, data=fetch_ngods_schema, status_code=200)
    except Exception:
        logger.exception("fetch_ngods")
        return build_response(success=False, error="An error occurred while fetching ngods", status_code=500)
@router.get(path="/search/{ngod_name}",
            description="Get a list of NGODs by name",
            response_model=FetchNGODsResponse)
async def get_ngod(ngod_name: str):
    try:
        ngods = await fetch_ngods_by_partial_name(ngod_name)
        ngod_schemas = [NGODSchema(**ngod) for ngod in ngods]
        fetch_ngods_schema = FetchNGODsSchema(ngods=ngod_schemas, total=len(ngod_schemas))
        return build_response(success=True, data=fetch_ngods_schema, status_code=200)
    except Exception:
        logger.exception("get_ngod")
        return build_response(success=False, error="An error occurred while fetching this ngod", status_code=500)