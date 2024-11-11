from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from bson import Binary
from app.schema.base import BodySchema, ResponseSchema
from app.common.constants import NOW
class FileDocumentSchema(BaseModel):
    filename: str = Field(...)
    file_data: str = Field(default_factory=lambda:"")
    content_type: str = Field(...)
class FileDocumentBody(BodySchema):
    data: FileDocumentSchema
class FileDocumentResponse(ResponseSchema):
    body: FileDocumentBody
class DownloadFileSchema(BaseModel):
    id: str = Field(...)