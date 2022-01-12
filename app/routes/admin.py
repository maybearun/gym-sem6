from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.sql.functions import mode
from starlette.responses import Response
from ..database import get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session, query
from typing import List

router=APIRouter(prefix="/admin",tags=['admin'])

# dashboard endpoint
# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def home()

#create_user
@router.post("/employees",status_code=status.HTTP_201_CREATED)
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
    print(new_dict)
    find_sal=new_dict['emp_type']
    query=db.query(models.Salary).filter(models.Salary.emp_type ==find_sal).first()
    print(query.salary_id)
    new_dict.pop("emp_type")
    new_dict['user_id']=users.user_id
    new_dict['salary_id']=query.salary_id
    print(new_dict)
    employee=models.Employee(**new_dict)
    query=db.add(employee)
    print(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/salaries",response_model=List[schemas.SalaryOut])
def get_salaries(db:Session=Depends(get_db)):
    get_sal=db.query(models.Salary).all()
    # print(get_sal)
    return get_sal


@router.post("/salaries",status_code=status.HTTP_201_CREATED)
def create_salary(payload:schemas.CreateSalary,db:Session=Depends(get_db)):

    query=db.query(models.Salary).filter(models.Salary.emp_type == payload.emp_type).first()
    if query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"the type {payload.emp_type} already exists in the database.")

    create_sal=models.Salary(**payload.dict())
    db.add(create_sal)
    db.commit()
    db.refresh(create_sal)
    return create_sal

@router.put("/salaries/{id}",response_model=schemas.SalaryOut)
def update_salary(id:int,payload:schemas.CreateSalary,db:Session=Depends(get_db)):
    update_sal=db.query(models.Salary).filter(models.Salary.salary_id==id)
    
    if update_sal.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the salary with id {id} was not found")
    
    update_sal.update(payload.dict())
    db.commit()
    return update_sal.first()

@router.delete("/salaries/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_salary(id:int,db:Session=Depends(get_db)):
    delete_sal=db.query(models.Salary).filter(models.Salary.salary_id==id)

    if delete_sal.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the salary with id {id} was not found")
    
    delete_sal.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)