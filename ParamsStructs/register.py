from pydantic import BaseModel, EmailStr,field_validator
import re
# from typing import Optional

class RegisterIn(BaseModel):
  username: str
  email: EmailStr
  password: str
  
  
  @field_validator("password")
  def validate_password_strength(cls, value):
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValueError("Password must contain at least one special character")
    return value


class SessionOut(BaseModel):
  id: int
  username: str
  email: EmailStr


class LoginIn(BaseModel):
  username: str
  password: str

class Config:
        orm_mode = True