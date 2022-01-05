from fastapi import APIRouter,HTTPException,status,Depends
from ..database import get_db
from .. import models,schemas
from sqlalchemy.orm import Session

router=APIRouter(prefix="admin",tags=['admin'])

# dashboard endpoint
# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def home()

