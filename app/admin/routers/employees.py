from fastapi import APIRouter, File, Form,HTTPException, UploadFile,status,Depends
from sqlalchemy.sql.functions import mode
from starlette.responses import Response
from app.database import get_db
from app import models,schemas,utils
from sqlalchemy.orm import Session
from typing import Any, List, Optional

router=APIRouter(prefix="/employees",tags=['employees'])


#get employees
@router.get("/")
def get_employees(db:Session=Depends(get_db)):
    get_emp=db.query(models.Employee).all()
    return get_emp

#create_user
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_employees(payload:schemas.CreateEmp,db:Session=Depends(get_db)):

    utils.check_if_employee_exists(payload.email_id,payload.primary_phone,payload.aadhar_no,payload.pan_no,db)

    hashed_password=utils.hashed(payload.password)
    payload.password=hashed_password

    users=models.Users(email_id=payload.email_id,password=payload.password)
    db.add(users)
    db.commit()
    db.refresh(users)

    invalid=["email_id","password"]
    new_dict=utils.without_keys(payload.dict(),invalid)
    # print(new_dict)
    find_sal=new_dict["emp_type"]
    query=db.query(models.Salary).filter(models.Salary.emp_type ==find_sal).first()
    # print(query.salary_id)
    new_dict.pop("emp_type")
    new_dict['user_id']=users.user_id
    new_dict['salary_id']=query.salary_id
    # if file:
    #     img_destination=utils.store_file('employee',file,payload.first_name)
    #     new_dict['photograph']=img_destination
    # print(new_dict)
    employee=models.Employee(**new_dict)
    db.add(employee)
    # print(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.get("/{id}")
def get_emp_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.Employee).filter(models.Employee.user_id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the Employee with id {id} was not found")
    return result

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
    # if file:
    #     img_destination=utils.store_file('member',file,payload.first_name)
    #     new_dict['photograph']=img_destination
    print(new_dict)
    updated_emp=db.query(models.Employee).filter(models.Employee.employee_id==id)
    updated_emp.update(new_dict,synchronize_session=False)
    db.commit()
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

