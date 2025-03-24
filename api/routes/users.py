from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..schemas import User

router = APIRouter(
    tags = ['Users Routes']
)

@router.get("/")
def get():
    return {"msg":"Hello World"}

@router.post("/register", response_description="Add new user")
async def create_user(user_info: User):
    user_info = jsonable_encoder(user_info)

# check for duplication
    username_found= await db["users"].find_one({"name": user_info["name"]})
    email_found = await db["users"].find_one({"email": user_info["email"]})
    
    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")
     
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return {"msg":"User created successfully", "data":created_user}
def get():
    return {"msg":"Hello World"}