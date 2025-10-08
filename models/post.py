from config.database import Base
from sqlalchemy import Column, Integer, String, Enum,ForeignKey
from config.database import get_db
from sqlalchemy.orm import relationship
import enum


class StatusEnum(enum.Enum):
    approve = "approve"
    reject = "reject"
    pending = "pending"



class Post(Base):
    __tablename__ = "posts"
    id= Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(StatusEnum, name="poststatus"), default=StatusEnum.pending)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post",cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post")
