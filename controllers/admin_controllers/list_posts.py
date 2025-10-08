from fastapi import APIRouter,Depends
from typing import List
from ParamsStructs.post import PostOut
from models.post import Post,StatusEnum
from config.database import get_db
from sqlalchemy.orm import Session
from utils.sessions import admin_required

router=APIRouter()

@router.get("/admin/posts/", response_model= List[PostOut])
def list_post_by_status(status: StatusEnum, db: Session = Depends(get_db),current_user: dict=Depends(admin_required)):
    posts = db.query(Post).filter(Post.status==status).all()
    return posts