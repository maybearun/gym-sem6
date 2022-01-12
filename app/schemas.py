from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import date, datetime

# for user login input
class Users(BaseModel):
    email:EmailStr
    password: str

# for token response
class Token(BaseModel):
    token:str
    token_type:str  

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
    
    class Config:
        orm_model=True
#for employee dashboard
class EmpOut(UserOut):
    aadhar_no:str
    pan_no:str
    designation:str

class CreateEmp(BaseModel):
    email_id:EmailStr
    password:str
    emp_type:str
    first_name:str
    last_name:str
    date_of_birth:date
    address:str
    state:str
    zip_code:str
    primary_phone:str
    additional_phone:str
    emergency_contact_name:str
    emergency_contact_phone:str
    photograph:str
    aadhar_no:str
    pan_no:str
    designation:str


#response model on creation of employee
class CreateEmpOut(BaseModel):
    email:EmailStr
    id:int
    first_name:str
    last_name:str
    designation:str
    
    class Config:
        orm_model=True

class CreateSalary(BaseModel):
    emp_type:str
    salary:float

class SalaryOut(BaseModel):
    salary_id:int
    emp_type:str
    salary:float
    timestamp:datetime
    
    class Config:
        orm_mode=True