import motor.motor_asyncio
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, EmailStr

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv("MONGODB_URL")
)
db = client.blog_api


# Convert BSON to JSON
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Define the user schema
class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "password"

            }
        }