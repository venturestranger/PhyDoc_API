from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import pymongo

router = APIRouter()

# DONT FORGET TO REPLACE "PASSWORD" WITH THE ACTUAL PASSWORD
client = pymongo.MongoClient("mongodb+srv://wispenjoyer:PASSWORD@clusterio.6bs83.mongodb.net/?retryWrites=true&w=majority&appName=clusterio")
db = client["mydatabase"]
users_collection = db["users"]

class User(BaseModel):
    user_id:    str
    initial_ts: int
    edit_ts: Optional[int] = None


@router.get("/{object_id}", response_model=User)
async def get_user(object_id: str):
    user = users_collection.find_one({"id": object_id})
    if user:
        return user
    raise HTTPException(status_code=404, detail="USER NOT FOUND")

@router.get("/", response_model=List[User])
async def get_users(field_name: Optional[str] = None, value: Optional[str] = None):
    query = {}
    if field_name and value:
        query[field_name] = value
    users = list(users_collection.find(query))
    return users

@router.post("/", response_model=User)
async def create_user(user: User):
    user.initial_ts = current_unix_timestamp()
    users_collection.insert_one(user.dict())
    return user

@router.put("/{object_id}", response_model=User)
async def update_user(object_id: str, user: User):
    user.edit_ts = current_unix_timestamp()
    result = users_collection.update_one({"id": object_id}, {"$set": user.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    return user

@router.delete("/{object_id}")
async def delete_user(object_id: str):
    result = users_collection.delete_one({"id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    return {"detail": "User deleted"}
