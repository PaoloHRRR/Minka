from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from app.schema.base import BodySchema, ResponseSchema
from app.common.constants import NOW
"""  POST SCHEMAS
"""
class ContentSchema(BaseModel):
    description: str = Field(..., min_length=1, description="Post description, cannot be empty")
    files: Optional[List[str]] = Field(default_factory=lambda: [], description="User's achievements")
    def __init__(self, **data):
        super().__init__(**data)

        if isinstance(self.files, List):
            for object_id in self.files:
                object_id = str(object_id)
class CommentSchema(BaseModel):
    user: str = Field(..., description="User who commented")
    date: Optional[datetime] = Field(default_factory=lambda: NOW(), description="Date when the comment was made")
    content: ContentSchema = Field(...,description="Content of the comment")

    def __init__(self, **data):
        super().__init__(**data)
        self.user = str(self.user)
class PostSchema(BaseModel):
    id: Optional[str] = Field(alias="_id")
    publisher: str = Field(..., description="Unique identifier for the publisher")
    publication_date: Optional[datetime] = Field(default_factory=lambda: NOW(), description="Date of post publication")
    content: ContentSchema = Field(...,description="Content of the post")
    comments: Optional[List[CommentSchema]] = Field(default_factory=lambda: [], description="User's achievements")
    def __init__(self, **data):
        super().__init__(**data)
        self.publisher = str(self.publisher)
class PostBody(BodySchema):
    data: PostSchema
class PostResponse(ResponseSchema):
    body: PostBody
"""  CREATE POST
"""
class RegisterPostSchema(BaseModel):
    publisher: str = Field(..., description="Unique identifier for the publisher")
    publication_date: Optional[datetime] = Field(default_factory=lambda: NOW(),description="Date of post publication")
    content: ContentSchema = Field(...,description="Content of the post")
""" FETCH ALL
"""
class FetchPostsSchema(BaseModel):
    posts: List[PostSchema] = []
    total: int = 0
class FetchPostsBody(BodySchema):
    data: FetchPostsSchema
class FetchPostsResponse(ResponseSchema):
    body: FetchPostsBody