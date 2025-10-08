from config.database import Base
from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")
    
    _table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_like"),)