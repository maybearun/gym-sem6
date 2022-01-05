from fastapi import FastAPI,HTTPException,Depends,APIRouter
from . import models
from .database import db_engine
from .routes import admin,trainer,receptionist,auth

models.Base.metadata.create_all(bind=db_engine)

app=FastAPI()

# setup routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(trainer.router)
app.include_router(receptionist.router)


