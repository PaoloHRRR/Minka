from fastapi import APIRouter, Body, Query
from loguru import logger
from app.common.utils import transform_mongo_document
from app.schema.base import build_response, SingleStringResponse, SingleStringSchema
from app.schema.ngod import *
from app.controller.ngod import *

router = APIRouter(
    prefix="/ngod",
    tags=["ngod"]
)
    
@router.get(path="/all", description="Fetch paginated ngods", response_model=FetchNGODsResponse)
async def fetch_ngods(
    page: int = Query(1, description="Page number, starts from 1"),
    limit: int = Query(50, description="Number of items per page")
):
    try:
        ngods = await fetch_paginated_ngods(page, limit)
        total_count = await database.NGODs.count_documents({})

        for ngod in ngods:
            ngod.pop("comments", None)

        ngod_schemas = [NGODSchema(**ngod) for ngod in ngods]

        fetch_ngods_schema = FetchNGODsSchema(
            ngods=ngod_schemas,
            total=total_count,
            page=page,
            total_pages=(total_count + limit - 1) // limit,
        )
        return build_response(success=True, data=fetch_ngods_schema, status_code=200)
    except Exception:
        logger.exception("fetch_ngods")
        return build_response(success=False, error="An error occurred while fetching ngods", status_code=500)

@router.get(
    path="/search/{ngod_name}",
    description="Get a list of NGODs by name",
    response_model=FetchNGODsResponse
)
async def get_ngod(ngod_name: str, page: int = 1, limit: int = 50):
    try:
        ngods, total_count = await fetch_paginated_ngods_by_partial_name(ngod_name, page, limit)
        
        ngod_schemas = [NGODSchema(**ngod) for ngod in ngods]
        fetch_ngods_schema = FetchNGODsSchema(
            ngods=ngod_schemas,
            total=total_count,
            page=page,
            total_pages=(total_count + limit - 1) // limit,
        )
        
        return build_response(success=True, data=fetch_ngods_schema, status_code=200)
    except Exception:
        logger.exception("fetch_ngods")
        return build_response(success=False, error="An error occurred while fetching ngods", status_code=500)
    
@router.get(path="-name/{ngod_id}",
            description="Get the name of a ngod by its id",
            response_model=SingleStringResponse)
async def get_ngod2(ngod_id: str):
    try:
        ngod_name = await get_ngod_name(ngod_id)
        if not ngod_name:
            return build_response(success=False, error="No records found", status_code=404)
        single_string_response = SingleStringSchema(name=ngod_name)
        return build_response(success=True, data=single_string_response, status_code=200)
        
    except Exception:
        return build_response(success=False, error="An error occurred while fetching this ngod", status_code=500)