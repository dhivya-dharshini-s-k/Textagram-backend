from fastapi import APIRouter,Depends,HTTPException
from ParamsStructs.post import PostUpdate
from sqlalchemy.orm import Session
from config.database import get_db
from models.post import Post, StatusEnum
from models.users import User
from utils.sessions import forbid_admin_user


router=APIRouter()

@router.put("/posts/{post_id}")
def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db),current_user:dict=Depends(forbid_admin_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id!=current_user["user_id"]:
        raise HTTPException(status_code=403, detail="You arenot allowed to edit this post")
    
    if post_data.content is not None:
        post.content = post_data.content
        post.status=StatusEnum.pending
    else:
        raise HTTPException(status_code=400, detail="No content to update")
    
 
    db.commit()
    db.refresh(post)
    return {
        "message": "Post updated successfully",
        "post": {
            "post_id": post.id,
            "content": post.content,
            "status": post.status.value,
            "user_id": post.user_id
        }
    }
