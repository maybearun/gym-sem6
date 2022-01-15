from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.sql.functions import mode
from starlette.responses import Response
from app.database import get_db
from app import models,schemas,utils
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(prefix="/admin/employees",tags=['employees'])


#get employees
@router.get("/")
def get_employees(db:Session=Depends(get_db)):
    get_emp=db.query(models.Employee).all()
    return get_emp

#create_user
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_employees(payload:schemas.CreateEmp,db:Session=Depends(get_db)):

    # check for email duplication
    query_email=db.query(models.Users).filter(models.Users.email_id==payload.email_id).first()
    if query_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {payload.email_id} already exist")
    # check for phone no. duplication
    query_phone=db.query(models.Employee).filter(models.Employee.primary_phone==payload.primary_phone).first()
    if query_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {payload.primary_phone} already exist")
    #check for aadhar duplication
    query_aadhar=db.query(models.Employee).filter(models.Employee.aadhar_no==payload.aadhar_no).first()
    if query_aadhar:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {payload.aadhar_no} already exist")
    #check for pan duplication
    query_pan=db.query(models.Employee).filter(models.Employee.pan_no==payload.pan_no).first()
    if query_pan:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"an account with {payload.pan_no} already exist")

    hashed_password=utils.hashed(payload.password)
    payload.password=hashed_password
    users=models.Users(email_id=payload.email_id,password=payload.password)
    db.add(users)
    db.commit()
    db.refresh(users)
    invalid=["email_id","password"]
    new_dict=utils.without_keys(payload.dict(),invalid)
    # print(new_dict)
    find_sal=new_dict['emp_type']
    query=db.query(models.Salary).filter(models.Salary.emp_type ==find_sal).first()
    print(query.salary_id)
    new_dict.pop("emp_type")
    new_dict['user_id']=users.user_id
    new_dict['salary_id']=query.salary_id
    # print(new_dict)
    employee=models.Employee(**new_dict)
    db.add(employee)
    # print(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.put("/{id}")
def update_employees(id:int,payload:schemas.CreateEmp,db:Session=Depends(get_db)):

    update_emp=db.query(models.Employee).filter(models.Employee.employee_id==id).first()
    if not update_emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the employee with id {id} was not found")
   
    hashed_password=utils.hashed(payload.password)
    payload.password=hashed_password
    user_id=update_emp.user_id
    db.query(models.Users).filter(models.Users.user_id==user_id).update({"email_id":payload.email_id,"password":payload.password})
    db.commit()

    invalid=["email_id","password"]
    new_dict=utils.without_keys(payload.dict(),invalid)
    # print(new_dict)
    find_sal=new_dict['emp_type']
    query=db.query(models.Salary).filter(models.Salary.emp_type ==find_sal).first()
    print(query.salary_id)
    new_dict.pop("emp_type")
    new_dict['salary_id']=query.salary_id
    print(new_dict)
    updated_emp=db.query(models.Employee).filter(models.Employee.employee_id==id)
    updated_emp.update(new_dict,synchronize_session=False)
    return updated_emp.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_employees(id:int,db:Session=Depends(get_db)):
    del_emp=db.query(models.Employee).filter(models.Employee.employee_id==id).first()
    if not del_emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the employee with the id {id} was not found")
    del_user=db.query(models.Users).filter(models.Users.user_id==del_emp.user_id)
    del_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

