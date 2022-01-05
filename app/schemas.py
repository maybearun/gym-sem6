from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import date, datetime

# for user login input
class Users(BaseModel):
    email:EmailStr
    password: str

# for user dashboard
class UserOut(Users):
    first_name:str
    last_name:str
    date_of_birth:str
    address:str
    zip_code:date
    primary_phone:str
    additional_phone:str
    emergency_contact_name:str
    emergency_contact_phone:str
    photograph:str
    
#for employee dashboard
class EmpOut(UserOut):
    aadhar_no:str
    pan_no:str
    designation:str

#response model on creation of employee
class CreateEmp(BaseModel):
    email:EmailStr
    id:int
    first_name:str
    last_name:str
  