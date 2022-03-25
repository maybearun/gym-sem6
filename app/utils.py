from fastapi import Depends
from passlib.context import CryptContext
from passlib.utils.decor import deprecated_method
from .database import get_db
from sqlalchemy.orm import Session
import os,shutil,uuid 
from fastapi import HTTPException,status
from pathlib import Path
from . import models

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

#for hashing passwords
def hashed(password:str):
    return pwd_context.hash(password)

# for verifing passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#for removing unwanted key values from dictionary
def without_keys(dict,invalid):
    return{x:dict[x] for x in dict if x not in invalid}

def check_if_employee_exists(email_id,primary_phone,aadhar_no,pan_no,db):
    # check for email duplication
    query_email=db.query(models.Users).filter(models.Users.email_id==email_id).first()
    if query_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {email_id} already exist")
    # check for phone no. duplication
    query_phone=db.query(models.Employee).filter(models.Employee.primary_phone==primary_phone).first()
    if query_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {primary_phone} already exist")
    #check for aadhar duplication
    query_aadhar=db.query(models.Employee).filter(models.Employee.aadhar_no==aadhar_no).first()
    if query_aadhar:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {aadhar_no} already exist")
    #check for pan duplication
    query_pan=db.query(models.Employee).filter(models.Employee.pan_no==pan_no).first()
    if query_pan:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {pan_no} already exist")

def store_file(user_type,upload_file,first_name):
    BASEDIR=os.path.dirname(__file__)
    _, ext = os.path.splitext(upload_file.filename)
    img_dir = os.path.join(BASEDIR, f'images/{user_type}/')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    if upload_file.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
        raise HTTPException(status_code=406, detail="Only .jpeg , .jpg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{first_name}{ext}'
    destination=Path(os.path.join(img_dir, file_name))
    try:
        with destination.open("wb+") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    return os.path.relpath(destination)

def check_if_member_exists(email_id,primary_phone,db):
    # check for email duplication
    query_email=db.query(models.Users).filter(models.Users.email_id==email_id).first()
    if query_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {email_id} already exist")
    # check for phone no. duplication
    query_phone=db.query(models.Members).filter(models.Members.primary_phone==primary_phone).first()
    if query_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {primary_phone} already exist")
    