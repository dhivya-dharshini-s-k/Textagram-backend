from ParamsStructs.register import RegisterIn, SessionOut
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from config.database import get_db
from models.users import User
from passlib.context import CryptContext


router = APIRouter()
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def register(userParams: RegisterIn, db: Session = Depends(get_db)):
  try:
    encrypted = crypt.hash(userParams.password)
    user = User(username=userParams.username, email=userParams.email, encrypted_password=encrypted, role_id=2)
    user.onCreateValidation(db)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
