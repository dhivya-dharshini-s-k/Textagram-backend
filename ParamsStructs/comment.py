from pydantic import BaseModel

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int

    class Config:
        orm_mode = True
