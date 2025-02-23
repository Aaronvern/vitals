from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.appwrite_service import db
from config import USERS_COLLECTION_ID, SECRET_KEY
from jose import jwt

router = APIRouter()
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
async def login(request: LoginRequest):
    users = db.list_documents(USERS_COLLECTION_ID, filters=[f"username={request.username}"])["documents"]
    
    if not users or users[0]["password"] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user = users[0]
    token = jwt.encode({"sub": user["$id"]}, SECRET_KEY, algorithm="HS256")
    
    return {"access_token": token, "token_type": "bearer"}
