from fastapi import FastAPI
from .routers import salaries,employees,auth,payroll,attendance


subapi = FastAPI(openapi_prefix="/admin")

subapi.include_router(auth.router)
subapi.include_router(employees.router)
subapi.include_router(salaries.router)
subapi.include_router(payroll.router)
subapi.include_router(attendance.router)
# dashboard endpoint
# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def home()

