from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from models.post import Post
from models.comments import Comment
from utils.sessions import forbid_admin_user
from ParamsStructs.comment import CommentUpdate, CommentOut

router=APIRouter()

@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, updated: CommentUpdate, db: Session = Depends(get_db), current_user: dict = Depends(forbid_admin_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    comment.content = updated.content
    db.commit()
    db.refresh(comment)
    return comment