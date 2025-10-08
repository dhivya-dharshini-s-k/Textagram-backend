from fastapi import APIRouter,Depends, HTTPException
from config.database import get_db
from models.users import User
from ParamsStructs.register import RegisterIn
from utils.sessions import admin_required, hash_password
from sqlalchemy.orm import Session

router=APIRouter()

@router.post("/admin/create-admin", status_code=201)
def create_admin(user_data: RegisterIn, db: Session = Depends(get_db), current_user: dict = Depends(admin_required)):
    
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_admin=User(
        username=user_data.username,
        email=user_data.email,
        encrypted_password = hash_password(user_data.password),
        role_id=1
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message":f"Admin user '{new_admin.username}' created successfully"}