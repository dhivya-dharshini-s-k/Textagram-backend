from fastapi import APIRouter,HTTPException,Depends
from utils.sessions import admin_required
from sqlalchemy.orm import Session
from config.database import get_db
from models.post import Post,StatusEnum

router = APIRouter()

@router.put("/admin/posts/{post_id}/approve")
def approve_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.status != StatusEnum.pending:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot Approve, Current status is '{post.status.value}'."
        )

    post.status = StatusEnum.approve
    db.commit()
    db.refresh(post)

    return {"message": f"Post {post_id} approved successfully"}
