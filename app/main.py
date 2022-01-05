from fastapi import FastAPI,HTTPException,Depends,APIRouter
from . import models
from .database import db_engine

models.Base.metadata.create_all(bind=db_engine)

app=FastAPI()

