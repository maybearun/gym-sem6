from email import message
from turtle import st
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import date, datetime

# for user login input
class Users(BaseModel):
    email:EmailStr
    password: str

# for token response
class Token(BaseModel):
    success:bool
    token:str
    token_type:str  

# for user dashboard
class UserOut(Users):
    first_name:str
    last_name:str
    date_of_birth:str
    address:str
    date_of_birth:date
    zip_code:str
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
    additional_phone:Optional[str]
    emergency_contact_name:str
    emergency_contact_phone:str
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

class CreatePayroll(BaseModel):
    emp_id:int
    account_id:int
    transaction_id:str

class CreateProduct(BaseModel):
    supplier_name:str
    product_title:str
    product_description:str
    product_price:float
    quantity:int

class CreateCommunityMsg(BaseModel):
    message_title:str
    message_description:str

class CreateSuppliers(BaseModel):
    supplier_name:str
    supplier_phone:str

class CreateLeave(BaseModel):
    leave_title:str
    leave_description:str
    status:Optional[str]=None
    employee_id:int
    applied_for:date

class CreateMembers(BaseModel):
    email_id:EmailStr
    password:str
    first_name:str
    last_name:str
    date_of_birth:date
    address:str
    state:str
    zip_code:str
    primary_phone:str
    additional_phone:Optional[str]
    emergency_contact_name:str
    emergency_contact_phone:str

class CreatePlans(BaseModel):
    plan_name:str
    plan_description:str
    plan_validity:int
    plan_price:float