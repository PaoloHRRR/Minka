from fastapi import File, UploadFile, APIRouter
from loguru import logger
from bson import Binary
import base64

from app.schema.base import build_response
from app.schema.file import (FileDocumentSchema, FileDocumentSchema2, FileDocumentResponse)
from app.controller.file import save_file, take_file
from app.common.utils import generate_unique_filename


router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post(path="/upload",
             description="Upload a file",
             response_model=FileDocumentResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()

        filedocumentschema = FileDocumentSchema(
            filename=generate_unique_filename(file.filename),
            content_type=file.content_type
        )

        file_dict = filedocumentschema.model_dump()
        file_dict["file_data"] = Binary(file_content)
        result = await save_file(file_dict)

        filedocumentschema2 = FileDocumentSchema2(_id=str(result), filename=filedocumentschema.filename, content_type=filedocumentschema.content_type)
        
        if not result:
            return build_response(success=False, error="An error occurred while uploading the file", status_code=500)
        
        return build_response(success=True, data=filedocumentschema2, status_code=201)
    except Exception:
        logger.exception("upload_file")
        return build_response(success=False, error="An error occurred while uploading the file", status_code=500)
    
@router.get(path="/download/{file_id}",
             description="Download a file")
async def download_file(file_id: str):
    file_document = await take_file(file_id)

    if file_document:
        file_data_base64 = base64.b64encode(file_document["file_data"]).decode("utf-8")
        return {
            "filename": file_document.get("filename", "unknown"),
            "content_type": file_document.get("content_type", "application/octet-stream"),
            "file_data_base64": file_data_base64
        }
    return {"error": "File not found"}
