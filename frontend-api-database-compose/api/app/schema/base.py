from datetime import datetime
from fastapi import Response
from loguru import logger
from pydantic import BaseModel
from typing import Any, Optional


class BodySchema(BaseModel):
    success: bool
    error: Optional[str] = None
    timestamp: datetime
    data: Any = None


class ResponseSchema(BaseModel):
    body: BodySchema


class SingleStringSchema(BaseModel):
    name: str


class SingleStringBody(BodySchema):
    data: SingleStringSchema


class SingleStringResponse(ResponseSchema):
    body: SingleStringBody


def build_response(success: bool,
                   status_code: int,
                   data: Any = None,
                   error: str = None):
    body = BodySchema(
        success=success,
        data=data,
        error=error,
        timestamp=datetime.now()
    )

    response = ResponseSchema(
        body=body
    ).model_dump_json()

    logger.info(response) if success else logger.error(response)
    return Response(content=response,
                    status_code=status_code,
                    media_type="application/json")