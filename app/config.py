from pydantic import BaseSettings

class Settings(BaseSettings):
    database_name:str
    database_password:str
    database_username:str
    database_hostname:str
    database_port:str
    secret_key:str
    algorithm:str
    expiration_time_in_minutes:int
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
settings=Settings()