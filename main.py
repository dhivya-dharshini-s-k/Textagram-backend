from fastapi import FastAPI
from controllers.session_controllers import register, login, seed_roles,seed_default_admin,list_all_posts,logout, guest
from controllers.post_controllers import create_post,list_post,update_post,delete_post
from controllers.session_controllers.protected import router as protected_router
from config.database import Base, engine, SessionLocal
from dotenv import load_dotenv
from controllers.admin_controllers import approve_post,reject_post,list_posts,create_new_admin
from controllers.likes_contollers import like_dislike,list_likes
from controllers.comments_controllers import comment_post, delete_comments, update_comments,list_comments
from fastapi.middleware.cors import CORSMiddleware 
 
 
load_dotenv()
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(guest.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(protected_router)
app.include_router(list_all_posts.router)
app.include_router(create_post.router)
app.include_router(list_post.router)
app.include_router(update_post.router)
app.include_router(delete_post.router)
app.include_router(approve_post.router)
app.include_router(reject_post.router)
app.include_router(list_posts.router)
app.include_router(create_new_admin.router)
app.include_router(like_dislike.router)
app.include_router(list_likes.router)
app.include_router(list_comments.router)
app.include_router(comment_post.router)
app.include_router(update_comments.router)
app.include_router(delete_comments.router)
app.include_router(logout.router)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        seed_roles.seed_roles(db)
        seed_default_admin.seed_default_admin(db) 
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"], 
)