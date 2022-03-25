from fastapi import HTTPException,Depends,APIRouter,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas,models,utils,oauth
from app.database import get_db

router=APIRouter(tags=['login'])

# login endpoint
@router.post("/login")
def login(payload:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    result=db.query(models.Users).filter(models.Users.email_id==payload.username).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with email {payload.username} was not found, please check the email entered")
    if not utils.verify_password(payload.password,result.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="please check password")
    token=oauth.create_token({"user_id":result.user_id})
    find_user_in_emp=db.query(models.Employee).filter(models.Employee.user_id==result.user_id).first()
    if find_user_in_emp:
        user_type="employee"
    else:
        user_type="member"
    return {"success":True,"token": token,"token_type":"bearer","user_type":user_type,"user_id":result.user_id}