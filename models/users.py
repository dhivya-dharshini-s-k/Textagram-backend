from config.database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime,ForeignKey,Boolean
from config.database import get_db
from sqlalchemy.orm import Session, relationship
import re
from pydantic import field_validator

class User(Base):
  __tablename__ = 'users'

  id=Column(Integer, primary_key=True)
  username=Column(String, unique=True, nullable=False)
  email=Column(String, unique=True, nullable=False)
  encrypted_password=Column(String, nullable=False)
  role_id=Column(Integer,ForeignKey("roles.id"),nullable=False)
  
  role=relationship("Role",back_populates="users")
  posts=relationship("Post",back_populates="user")
  comments=relationship("Comment",back_populates="user", cascade="all, delete-orphan")
  likes=relationship("Like",back_populates="user")
  
  

  def onCreateValidation(self, db: Session):

    if db.query(User).filter(User.email == self.email).count() != 0:
      raise Exception("email already taken")


    if db.query(User).filter(User.username == self.username).count() != 0:
      raise Exception("username already taken")
