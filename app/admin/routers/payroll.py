from fastapi import APIRouter,HTTPException,status,Depends
from app.database import get_db
from app import models,schemas,oauth
from sqlalchemy.orm import Session

router=APIRouter(prefix="/payroll",tags=['payroll'])

@router.get("/")
def get_payroll(db:Session=Depends(get_db),user_id:int =Depends(oauth.get_current_user)):

    get_pay=db.query(models.Payroll).all()
    return get_pay

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_payroll(payload:schemas.CreatePayroll,db:Session=Depends(get_db),user_id:int =Depends(oauth.get_current_user)):

    create_payroll=models.Salary(**payload.dict())
    db.add(create_payroll)
    db.commit()
    db.refresh(create_payroll)
    return create_payroll
