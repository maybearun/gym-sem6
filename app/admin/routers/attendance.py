from fastapi import APIRouter,HTTPException,status,Depends
from app.database import get_db
from app import models,schemas,oauth
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(prefix="/attendance",tags=['attendance'])

@router.get("/")
def get_attendance(db:Session=Depends(get_db)):

    get_attend=db.query(models.EmployeeAttendance).all()
    return get_attend
