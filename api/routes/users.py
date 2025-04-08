from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from api.schemas import UserCreate, UserResponse
from database import get_database
from utils import hash_password
import secrets
import logging

router = APIRouter(tags=["Users Routes"])

# ❌ This was the problematic line before:
# async def get_db(app: FastAPI = Depends()):
# ✅ Fixed:
async def get_db():
    db = await get_database()
    return db

@router.post("/users", response_description="Add new user", response_model=UserResponse)
async def create_user(user_info: UserCreate, db=Depends(get_db)):
    user_info = jsonable_encoder(user_info)
    logging.info(f"Received user data: {user_info}")

    if await db["users"].find_one({"name": user_info["name"]}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    if await db["users"].find_one({"email": user_info["email"]}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    user_info["password"] = hash_password(user_info["password"])
    user_info["apiKey"] = secrets.token_hex(30)

    try:
        result = await db["users"].insert_one(user_info)
        created_user = await db["users"].find_one({"_id": result.inserted_id})

        response_user = {
            "_id": created_user["_id"],
            "name": created_user["name"],
            "email": created_user["email"]
        }

        logging.info(f"Inserted user with ID: {result.inserted_id}")
        return UserResponse(**response_user)

    except Exception as e:
        logging.error(f"Database insertion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )
