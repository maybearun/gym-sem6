from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.sql.functions import mode
from starlette.responses import Response
from app.database import get_db
from app import models,schemas,utils
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(prefix="/admin/salaries",tags=['salary'])

#salaries
@router.get("/",response_model=List[schemas.SalaryOut])
def get_salaries(db:Session=Depends(get_db)):
    get_sal=db.query(models.Salary).all()
    # print(get_sal)
    return get_sal

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_salary(payload:schemas.CreateSalary,db:Session=Depends(get_db)):

    query=db.query(models.Salary).filter(models.Salary.emp_type == payload.emp_type).first()
    if query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"the type {payload.emp_type} already exists in the database.")

    create_sal=models.Salary(**payload.dict())
    db.add(create_sal)
    db.commit()
    db.refresh(create_sal)
    return create_sal

@router.put("/{id}",response_model=schemas.SalaryOut)
def update_salary(id:int,payload:schemas.CreateSalary,db:Session=Depends(get_db)):
    update_sal=db.query(models.Salary).filter(models.Salary.salary_id==id)
    
    if update_sal.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the salary with id {id} was not found")
    
    update_sal.update(payload.dict(),synchronize_session=False)
    db.commit()
    return update_sal.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_salary(id:int,db:Session=Depends(get_db)):
    delete_sal=db.query(models.Salary).filter(models.Salary.salary_id==id)

    if delete_sal.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the salary with id {id} was not found")
    
    delete_sal.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)