from ParamsStructs.register import SessionOut, LoginIn
from fastapi import Depends, HTTPException, APIRouter, status, Response
from sqlalchemy.orm import Session
from config.database import get_db
from models.users import User
from passlib.context import CryptContext
from utils.sessions import generate_token

router = APIRouter()
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=SessionOut, status_code=status.HTTP_200_OK)
def login(res: Response, userParams: LoginIn, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == userParams.username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        if not crypt.verify(userParams.password, user.encrypted_password):
            raise HTTPException(status_code=401, detail="Invalid password")
        
        try:
            token = generate_token(user)
        except Exception:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token is not valid."
        )
        
        res.headers['Authorization'] = f"Bearer {token}"
        return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail="Internal server error")
