from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import redis
import jwt
import uuid
from fastapi import HTTPException, status, Depends
from utils.auth import get_current_user

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)



def generate_token(user):
    secret_key = os.getenv("SECRET_KEY")
    expires_at_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINS", 30)) 

    expires = datetime.utcnow() + timedelta(minutes=expires_at_minutes)
    jti = str(uuid.uuid4())

    payload = {
        "user_id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "exp": expires,
        "jti": jti 
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token
  
  

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role_id"] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def blacklist_token(jti: str, expires_in: int):
    redis_client.setex(jti, expires_in, "true")

def get_token_from_header(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization Header"
        )
    return auth_header.split(" ")[1]




def forbid_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role_id") == 1:  
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins are not allowed to perform this action."
        )
    return current_user
