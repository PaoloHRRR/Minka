from bson import ObjectId
import uuid
import time
import os

def transform_mongo_document(data: dict):
    if isinstance(data, dict):
        return {key: transform_mongo_document(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [transform_mongo_document(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data
    
def generate_unique_filename(original_filename: str) -> str:
    _, extension = os.path.splitext(original_filename)
    
    timestamp = int(time.time() * 1000)

    unique_id = uuid.uuid4().hex
    
    unique_filename = f"{timestamp}_{unique_id}{extension}"
    
    return unique_filename

def transform_mongo_document(data: dict):
    if isinstance(data, dict):
        return {key: transform_mongo_document(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [transform_mongo_document(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data