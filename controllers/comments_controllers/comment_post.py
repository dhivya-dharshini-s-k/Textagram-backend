from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from models.post import Post,StatusEnum
from models.comments import Comment
from utils.sessions import get_current_user, forbid_admin_user
from ParamsStructs.comment import CommentCreate, CommentOut
from models.users import User
from utils.sessions import forbid_admin_user
router=APIRouter()

@router.post("/posts/{post_id}/comment", response_model=CommentOut)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(forbid_admin_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status != StatusEnum.approve:
        raise HTTPException(status_code=403, detail="Cannot comment on unapproved post")
    
    new_comment = Comment(
        content=comment.content,
        post_id=post_id,
        user_id=current_user["user_id"]
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment