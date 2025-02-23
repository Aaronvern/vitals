from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from config import SECRET_KEY, USERS_COLLECTION_ID
from database import get_document, list_documents, create_document


class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    wallet_address: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_document(USERS_COLLECTION_ID, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def login(request: LoginRequest):
    users = list_documents(USERS_COLLECTION_ID, filters=[f"username={request.username}"])["documents"]
    if not users or users[0]["password"] != request.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user = users[0]
    token = jwt.encode({"sub": user["$id"]}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

def register(request: RegisterRequest):
    users = list_documents(USERS_COLLECTION_ID, filters=[f"username={request.username}"])["documents"]
    if users:
        raise HTTPException(status_code=400, detail="Username exists")
    user = create_document(
        USERS_COLLECTION_ID,
        {"username": request.username, "password": request.password, "wallet_address": request.wallet_address}
    )
    token = jwt.encode({"sub": user["$id"]}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}