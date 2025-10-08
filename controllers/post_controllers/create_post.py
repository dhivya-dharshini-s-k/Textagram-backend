from models.post import Post,StatusEnum
from ParamsStructs.post import PostCreate,PostOut
from fastapi import Depends, HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from config.database import get_db
from utils.sessions import forbid_admin_user
router=APIRouter()

@router.post("/post", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def CreatePost(post_in: PostCreate, db: Session = Depends(get_db),current_user: dict = Depends(forbid_admin_user)):
    post = Post(
        content= post_in.content,
        status=StatusEnum.pending,  
        user_id=current_user["user_id"]
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    

    return post
    