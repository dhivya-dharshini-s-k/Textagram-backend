from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from config.database import get_db
from models.post import Post
from models.likes import Like
from models.comments import Comment
from models.users import User
from collections import defaultdict

router = APIRouter()

@router.get("/all-posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = (
        db.query(
            Post.id.label("post_id"),
            Post.content,
            Post.status,
            func.count(Like.id).label("like_count")
        )
        .outerjoin(Like, Like.post_id == Post.id)
        .filter(Post.status == "approve")
        .group_by(Post.id)
        .all()
    )

    post_ids = [p.post_id for p in posts] 

    
    comments = (
        db.query(
            Comment.post_id,
            Comment.id.label("comment_id"),
            Comment.content.label("comment_content"),
            User.id.label("user_id"),
            User.username,
        )
        .join(User, Comment.user_id == User.id)
        .filter(Comment.post_id.in_(post_ids))
        .all()
    )

    comment_dict = defaultdict(list)

    for c in comments:
        comment_dict[c.post_id].append({
            "comment_id": c.comment_id,
            "content": c.comment_content,
            "user_id": c.user_id,
            "username": c.username
        })
    return [
        {
            "post_id": p.post_id,
            "content": p.content,
            "status": p.status,
            "like_count": p.like_count,
            "comments": comment_dict.get(p.post_id, [])
        }
        for p in posts
    ]


    