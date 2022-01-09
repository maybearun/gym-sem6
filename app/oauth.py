#this is to protect the application from unautorized useage

from fastapi import Depends,status, HTTPException
from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.sql.functions import user
from . import schemas
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
EXPIRATION_TIME_IN_MINUTES=settings.expiration_time_in_minutes

#to generate the JWT for a user 
def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_IN_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#verify the jwt of the user
def verify_token(token:str, credential_exception):
    
    try:

        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        #if no id then the user is not a vaild user hence throw error
        if id is None:
            raise credential_exception

        token_data=schemas.TokenData(id=id)
    except JWTError :
        raise credential_exception

    return token_data

def get_current_user(token:str= Depends(oauth2_scheme)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to do this task",headers={"WWW-Authenticate":"Bearer"})

    return verify_token(token,credential_exception)
