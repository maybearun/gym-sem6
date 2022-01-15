from fastapi import FastAPI
from .routers import salaries,employees,auth


subapi = FastAPI(openapi_prefix="/admin")

subapi.include_router(auth.router)
subapi.include_router(employees.router)
subapi.include_router(salaries.router)

# dashboard endpoint
# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def home()

