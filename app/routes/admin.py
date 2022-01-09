from fastapi import APIRouter,HTTPException,status,Depends
from starlette.responses import Response
from ..database import get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(prefix="/admin",tags=['admin'])

# dashboard endpoint
# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def home()

#create_user
@router.post("/employees",status_code=status.HTTP_201_CREATED)
def create_employees(payload:schemas.CreateEmp,db:Session=Depends(get_db)):

    hashed_password=utils.hashed(payload.password)
    payload.password=hashed_password
    users=models.Users(email_id=payload.email_id,password=payload.password)
    db.add(users)
    db.commit()
    # db.refresh(users)
    # return users
    # invalid=["email_id","password"]
    # new_dict=utils.without_keys(payload.dict(),invalid)
    # print(new_dict)
    # employee=models.Employee(**new_dict.dict())
    # query=db.add(employee)
    # print(employee)
    # db.commit()
    # db.refresh(employee)
    # return {employee}


@router.get("/salaries",response_model=List[schemas.SalaryOut])
def get_salaries(db:Session=Depends(get_db)):
    get_sal=db.query(models.Salary).all()
    # print(get_sal)
    return get_sal


@router.post("/salaries",status_code=status.HTTP_201_CREATED)
def create_salary(payload:schemas.CreateSalary,db:Session=Depends(get_db)):
    create_sal=models.Salary(**payload.dict())
    db.add(create_sal)
    db.commit()
    db.refresh(create_sal)
    return create_sal

@router.put("/salaries/{id}",response_model=schemas.SalaryOut)
def update_salary(id:int,payload:schemas.CreateSalary,db:Session=Depends(get_db)):
    update_sal=db.query(models.Salary).filter(models.Salary.salary_id==id)
    
    if update_sal.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the product with id {id} was not found")
    
    update_sal.update(payload.dict())
    db.commit()
    return update_sal.first()

@router.delete("/salaries/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_salary(id:int,db:Session=Depends(get_db)):
    delete_sal=db.query(models.Salary).filter(models.Salary.salary_id==id)

    if delete_sal.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the product with id {id} was not found")
    
    delete_sal.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)