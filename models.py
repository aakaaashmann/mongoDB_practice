from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    id: str
    city: str

class User(BaseModel):
    id: str
    name: str
    age: int
    address_id: Optional[str] = None    
    address: Optional[Address] = None
    
    class Config:
        orm_mode = True

