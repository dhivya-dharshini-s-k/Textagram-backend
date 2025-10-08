from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ParamsStructs.guest import GuestPostOut
from config.database import get_db
from models.post import Post
from models.likes import Like
from sqlalchemy import func


router = APIRouter()


@router.get("/guest-user", response_model=List[GuestPostOut])
def list_all_posts(db: Session = Depends(get_db)):

    posts = (
        db.query(Post)
        .outerjoin(Post.likes) 
        .group_by(Post.id, Post.user_id)  
        .group_by(Post.id)
        .order_by(func.count(Like.id).desc())
        .limit(3)
        .all()
    )
    response = []
    for post in posts:
        response.append({
            "username": post.user.username,
            "post_id": post.id,
            "content": post.content, 
            "likes": len(post.likes) if post.likes else 0,
            "comments": len(post.comments) if post.comments else 0,
        })

    return response
