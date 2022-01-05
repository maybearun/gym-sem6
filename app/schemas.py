from pydantic import BaseModel
from pydantic.networks import EmailStr

class Users(BaseModel):
    email:EmailStr
    password: str

class Employee(Users):
    pass