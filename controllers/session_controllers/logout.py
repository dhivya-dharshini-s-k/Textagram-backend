from fastapi import APIRouter, Request, HTTPException, status,Response
from jose import jwt,JWTError
from datetime import datetime, timezone
from utils.sessions import get_token_from_header, blacklist_token 
import redis,os

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


@router.post("/logout")
def logout(request: Request):
    token = get_token_from_header(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp_timestamp = payload.get("exp")
        if not jti or not exp_timestamp:
            raise HTTPException(status_code=400, detail="Invalid token")

        expires_in = exp_timestamp - int(datetime.now(timezone.utc).timestamp())
        if expires_in > 0:
            blacklist_token(jti, expires_in)

        return {"message": "Successfully logged out"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    