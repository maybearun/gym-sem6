from webbrowser import get
from fastapi import APIRouter, File, Form,HTTPException, UploadFile,status,Depends
from sqlalchemy.sql.functions import mode
from starlette.responses import Response
from app.database import get_db
from app import models,schemas,utils
from sqlalchemy.orm import Session
from typing import Any, List, Optional


router=APIRouter(prefix="/members",tags=['members'])

@router.get("/")
def get_members(db:Session=Depends(get_db)):
    get_member=db.query(models.Members).all()
    return get_member

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_members(payload:schemas.CreateMembers,db:Session=Depends(get_db)):

    utils.check_if_member_exists(payload.email_id,payload.primary_phone,db)

    hashed_password=utils.hashed(payload.password)
    payload.password=hashed_password

    users=models.Users(email_id=payload.email_id,password=payload.password)
    db.add(users)
    db.commit()
    db.refresh(users)

    invalid=["email_id","password"]
    new_dict=utils.without_keys(payload.dict(),invalid)
    # print(new_dict)
    # find_sal=new_dict["emp_type"]
    # query=db.query(models.Salary).filter(models.Salary.emp_type ==find_sal).first()
    # # print(query.salary_id)
    # new_dict.pop("emp_type")
    new_dict['user_id']=users.user_id
    # new_dict['salary_id']=query.salary_id
    # if file:
    #     img_destination=utils.store_file('member',file,payload.first_name)
    #     new_dict['photograph']=img_destination
    # print(new_dict)
    member=models.Members(**new_dict)
    db.add(member)
    # print(employee)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{id}")
def get_member_by_id(id:int,db:Session=Depends(get_db)):
#     SELECT * FROM members  JOIN users ON users.user_id = members.user_id
# WHERE members.member_id = 3
    result=db.query(models.Members).filter(models.Members.user_id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the Member with id {id} was not found")
    # print(result)
    return result
    

@router.put("/{id}")
def update_members(id:int,payload:schemas.CreateMembers,db:Session=Depends(get_db)):

    update_member=db.query(models.Members).filter(models.Members.member_id==id).first()
    if not update_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the member with id {id} was not found")
   
    hashed_password=utils.hashed(payload.password)
    payload.password=hashed_password
    user_id=update_member.user_id
    db.query(models.Users).filter(models.Users.user_id==user_id).update({"email_id":payload.email_id,"password":payload.password})
    db.commit()

    invalid=["email_id","password"]
    new_dict=utils.without_keys(payload.dict(),invalid)
    # print(new_dict)
    # if file:
    #     img_destination=utils.store_file('member',file,payload.first_name)
    #     new_dict['photograph']=img_destination
    updated_mem=db.query(models.Members).filter(models.Members.member_id==id)
    updated_mem.update(new_dict,synchronize_session=False)
    db.commit()
    return updated_mem.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_employees(id:int,db:Session=Depends(get_db)):
    del_emp=db.query(models.Members).filter(models.Members.member_id==id).first()
    if not del_emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the employee with the id {id} was not found")
    del_user=db.query(models.Users).filter(models.Users.user_id==del_emp.user_id)
    del_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)