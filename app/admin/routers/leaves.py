from typing import Optional
from fastapi import APIRouter,HTTPException, UploadFile,status,Depends,File,Response
from app.database import get_db
from app import models,schemas,oauth,utils
from sqlalchemy.orm import Session

router=APIRouter(prefix="/leave",tags=['leave'])

@router.get("/")
def get_leave(db:Session=Depends(get_db)):

    get_leave=db.query(models.Leave).all()
    return get_leave


@router.post("/",status_code=status.HTTP_201_CREATED)
def create_leave(payload:schemas.CreateLeave,db:Session=Depends(get_db)):
    create_leave=models.Leave(**payload.dict())
    db.add(create_leave)
    db.commit()
    db.refresh(create_leave)
    return create_leave

@router.get("/{id}")
def get_leave_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.Leave).filter(models.Leave.id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the Leave with id {id} was not found")
    return result
    
@router.put("/{id}")
def update_leave(id:int,payload:schemas.CreateLeave,db:Session=Depends(get_db)):

    update_leave=db.query(models.Leave).filter(models.Leave.leave_id==id)
    if not update_leave.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the leave application with id {id} was not found")
    
    
    update_leave.update(payload.dict())
    db.commit()

    return update_leave.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_leave(id:int,db:Session=Depends(get_db)):

    delete_leave=db.query(models.Leave).filter(models.Leave.leave_id==id)
    if not delete_leave.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the supplier with id {id} was not found")

    delete_leave.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
