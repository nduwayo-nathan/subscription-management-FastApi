from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    password: str  # Include password for creation and updates

class UserCreate(UserBase):
    pass  # Required during creation

class UserUpdate(BaseModel):
    email: Optional[str] = None  # Make email field optional
    password: Optional[str] = None  # Make password optional for updates

class User(UserBase):
    id: int

    class Config:
        orm_mode = True  # Pydantic will use the SQLAlchemy model as a dict
        fields = {
            'password': {'exclude': True}  # Exclude the password field from the response
        }
