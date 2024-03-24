from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str