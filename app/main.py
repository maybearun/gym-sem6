import imp
from fastapi import FastAPI,HTTPException,Depends,APIRouter
from . import models
from .database import db_engine
from .routes import admin,trainer,receptionist,auth
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=db_engine)

app=FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# setup routers
app.include_router(auth.router)
app.include_router(admin.router)
# app.include_router(trainer.router)
# app.include_router(receptionist.router)


