from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from models.post import Post
from models.likes import Like

router=APIRouter()

@router.get("/posts/{post_id}/likes")
def list_likes(post_id: int, db: Session = Depends(get_db)):
    post=db.query(Post).filter(Post.id ==post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not found")
    
    likes = db.query(Like).filter_by(post_id=post_id).all()
    user_ids=[like.user_id for like in likes]
    
    return{
        "post_id":post_id,
        "like_count": len(likes),
        "liked_by_user_ids":user_ids
    }