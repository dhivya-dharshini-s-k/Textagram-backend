from pydantic import BaseModel

class GuestPostOut(BaseModel):
    username: str
    post_id: int
    content: str
    likes: int
    comments: int

    class Config:
        orm_mode = True