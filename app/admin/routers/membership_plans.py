from typing import Optional
from fastapi import APIRouter,HTTPException, Response, UploadFile,status,Depends,File
from app.database import get_db
from app import models,schemas,oauth,utils
from sqlalchemy.orm import Session

router=APIRouter(prefix="/membership_plans",tags=['membership plans'])

@router.get("/")
def get_plans(db:Session=Depends(get_db)):

    get_plan=db.query(models.MembershipPlans).all()
    return get_plan

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_plans(payload:schemas.CreatePlans,db:Session=Depends(get_db)):

    query=db.query(models.MembershipPlans).filter(models.MembershipPlans.plan_name == payload.plan_name).first()
    if query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"the plan {payload.plan_name} already exists in the database.")

    create_plan=models.MembershipPlans(**payload.dict())
    db.add(create_plan)
    db.commit()
    db.refresh(create_plan)
    return create_plan

@router.get("/{id}")
def get_plan_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.MembershipPlans).filter(models.MembershipPlans.id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the plan with id {id} was not found")
    return result
    
@router.put("/{id}")
def update_plans(id:int,payload:schemas.CreatePlans,db:Session=Depends(get_db)):

    update_plan=db.query(models.MembershipPlans).filter(models.MembershipPlans.plan_id==id)
    
    if update_plan.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the plan with id {id} was not found")
    
    update_plan.update(payload.dict(),synchronize_session=False)
    db.commit()
    return update_plan.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_plans(id:int,db:Session=Depends(get_db)):
    delete_plan=db.query(models.MembershipPlans).filter(models.MembershipPlans.plan_id==id)

    if delete_plan.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the plan with id {id} was not found")
    
    delete_plan.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)