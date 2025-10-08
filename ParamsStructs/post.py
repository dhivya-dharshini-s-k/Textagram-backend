from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class StatusEnumStr(str, Enum):
    approve = "approve"
    reject = "reject"
    pending = "pending"

class PostCreate(BaseModel):
    content: str

class PostUpdate(BaseModel):
    content: Optional[str]
    

class PostOut(BaseModel):
    post_id: int= Field(..., alias="id")
    content: str
    status: StatusEnumStr
    user_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  
