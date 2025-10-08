from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from config.database import get_db
from ParamsStructs.post import PostOut
from utils.sessions import forbid_admin_user
from models.post import Post
from typing import List

router=APIRouter()

@router.get("/posts/me", response_model=List[PostOut])
def list_my_posts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(forbid_admin_user)
):
    posts = db.query(Post).filter(Post.user_id == current_user["user_id"]).all()
    return posts
