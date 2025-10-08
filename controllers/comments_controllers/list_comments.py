from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from models.post import Post
from models.comments import Comment
from ParamsStructs.comment import CommentOut

router=APIRouter()

@router.get("/posts/{post_id}/comments",response_model=list[CommentOut])
def list_posts(post_id: int,db:Session =Depends(get_db)):
    post=db.query(Post).filter(Post.id ==post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not found")
    
    comments = db.query(Comment).filter_by(post_id=post_id).all()
    return comments
    
    
    