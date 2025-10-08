from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from models.post import Post,StatusEnum
from models.likes import Like
from utils.sessions import forbid_admin_user

router=APIRouter()


@router.post("/posts/{post_id}/like")
def like_dislike_post(post_id: int, db:Session=Depends(get_db),current_user: dict=Depends(forbid_admin_user)):
    post=db.query(Post).filter(Post.id == post_id).first()
    if not post:
         raise HTTPException(status_code=404, detail="Post not found")
     
    if post.status != StatusEnum.approve:
        raise HTTPException(status_code=403, detail="Cannot like unapproved post")

    existing_like = db.query(Like).filter_by(post_id=post_id, user_id=current_user["user_id"]).first()
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return{"message": "Post unliked"}
    else:
        new_like=Like(post_id = post_id, user_id=current_user["user_id"])
        db.add(new_like)
        db.commit()
        return {"message":"Post Liked"}
    
    