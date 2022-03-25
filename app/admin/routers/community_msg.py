from typing import Optional
from fastapi import APIRouter,HTTPException, UploadFile,status,Depends,File,Response
from app.database import get_db
from app import models,schemas,oauth,utils
from sqlalchemy.orm import Session

router=APIRouter(prefix="/community_msg",tags=['community messages'])

@router.get("/")
def get_msgs(db:Session=Depends(get_db)):

    get_msg=db.query(models.CommunityMessage).all()
    return get_msg

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_msgs(payload:schemas.CreateCommunityMsg,db:Session=Depends(get_db)):
    create_msg=models.CommunityMessage(**payload.dict())
    db.add(create_msg)
    db.commit()
    db.refresh(create_msg)
    return create_msg

@router.get("/{id}")
def get_msg_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.CommunityMessage).filter(models.CommunityMessage.id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the message with id {id} was not found")
    return result

@router.put("/{id}")
def update_msgs(id:int,payload:schemas.CreateCommunityMsg,db:Session=Depends(get_db)):

    update_msg=db.query(models.CommunityMessage).filter(models.CommunityMessage.message_id==id)
    if not update_msg.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the leave application with id {id} was not found")
    
    
    update_msg.update(payload.dict())
    db.commit()

    return update_msg.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_msgs(id:int,db:Session=Depends(get_db)):
    
    delete_msg=db.query(models.CommunityMessage).filter(models.CommunityMessage.message_id==id)
    if not delete_msg.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the supplier with id {id} was not found")

    delete_msg.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
