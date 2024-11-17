from datetime import datetime
from fastapi import APIRouter, Body
from loguru import logger

from app.common.utils import transform_mongo_document
from app.schema.base import build_response, SingleStringSchema, SingleStringResponse
from app.schema.user import (UserSchema, UserResponse,
                                FetchUsersSchema, FetchUsersResponse,
                                RegisterSchema,
                                LoginSchema, TokenSchema, TokenResponse)
from app.controller.user import (fetch_all_users, fetch_user_by_email, create_user, get_user_name)
from app.common.security import (verify_password, create_access_token)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(path="/all",
            description="Fetch all users",
            response_model=FetchUsersResponse)
async def fetch_users():
    try:
        users = await fetch_all_users()
        user_schemas = [UserSchema(**transform_mongo_document(user)) for user in users]
        fetch_users_schema = FetchUsersSchema(users=user_schemas, total=len(user_schemas))
        return build_response(success=True, data=fetch_users_schema, status_code=200)
    except Exception:
        logger.exception("fetch_users")
        return build_response(success=False, error="An error occurred while fetching users", status_code=500)


@router.post(path="/register",
             description="Register a new user",
             response_model=UserResponse)
async def register(user: RegisterSchema = Body(...)):
    try:
        existing_user = await fetch_user_by_email(user.email)
        if existing_user:
            return build_response(success=False, error="Email is already taken", status_code=400)
        
        user_dict = user.model_dump()
        _id = await create_user(user_dict)
        if not _id:
            return build_response(success=False, error="An error occurred while registering the user", status_code=500)
        
        user_schema = UserSchema(**transform_mongo_document(user_dict))
        return build_response(success=True, data=user_schema, status_code=200)
    except Exception:
        logger.exception("create_user")
        return build_response(success=False, error="An error occurred while creating a new user", status_code=500)


@router.post(path="/login",
             description="Log into an existing account",
             response_model=TokenResponse)
async def login(user: LoginSchema = Body(...)):
    try:
        existing_user = await fetch_user_by_email(user.email)
        if not existing_user:
            return build_response(success=False, error="No account found with this email address", status_code=400)

        if not verify_password(user.password, existing_user["password"]):
            return build_response(success=False, error="Incorrect credentials", status_code=401)
        else:
            access_token = create_access_token(data={"sub": user.email})
            token_schema = TokenSchema(access_token=access_token, id=str(existing_user["_id"]), email=existing_user["email"], system_role=existing_user["system_role"], name=existing_user["name"])
            return build_response(success=True, data=token_schema, status_code=200)

    except Exception:
        logger.exception("login")
        return build_response(success=False, error="An error occurred while logging", status_code=500)
    
@router.get(path="-name/{user_id}",
            description="Get the name of an user by its id",
            response_model=SingleStringResponse)
async def get_user2(user_id: str):
    try:
        user_name = await get_user_name(user_id)
        if not user_name:
            return build_response(success=False, error="No records found", status_code=404)
        single_string_response = SingleStringSchema(name=user_name)
        return build_response(success=True, data=single_string_response, status_code=200)
        
    except Exception:
        return build_response(success=False, error="An error occurred while fetching this user", status_code=500)