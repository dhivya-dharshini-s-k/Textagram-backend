from fastapi import APIRouter,Depends,HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from utils.sessions import forbid_admin_user
from models.post import Post

router=APIRouter()

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(forbid_admin_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
