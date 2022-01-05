from fastapi import HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas,models,utils
from database import get_db
router=APIRouter()

# login endpoint
@router.post("/login",)
def login(payload:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return {"details":"login successful"}