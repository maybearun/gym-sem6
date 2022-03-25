from fastapi import APIRouter,HTTPException,status,Depends
from app.database import get_db
from app import models,schemas,oauth
from sqlalchemy.orm import Session

router=APIRouter(prefix="/payroll",tags=['payroll'])

@router.get("/")
def get_payroll(db:Session=Depends(get_db)):

    get_pay=db.query(models.Payroll).all()
    return get_pay

@router.get("/{id}")
def get_payroll_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.Payroll).filter(models.Payroll.id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the Payroll with id {id} was not found")
    return result
    
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_payroll(payload:schemas.CreatePayroll,db:Session=Depends(get_db)):

    create_payroll=models.Payroll(**payload.dict())
    db.add(create_payroll)
    db.commit()
    db.refresh(create_payroll)
    return create_payroll
