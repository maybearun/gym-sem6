from passlib.context import CryptContext
from passlib.utils.decor import deprecated_method

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

#for hashing passwords
def hashed(password:str):
    return pwd_context.hash(password)

# for verifing passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)