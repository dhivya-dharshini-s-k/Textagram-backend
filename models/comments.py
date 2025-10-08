from config.database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime,ForeignKey,Boolean
from config.database import get_db
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__="comments"
    id= Column(Integer,primary_key=True)
    content=Column(String,nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")