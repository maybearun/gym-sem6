from fastapi import FastAPI
from .routers import salaries,employees,auth,payroll,attendance,product,supplier,community_msg,leaves,members,membership_plans


subapi = FastAPI(openapi_prefix="/admin")

subapi.include_router(auth.router)
subapi.include_router(employees.router)
subapi.include_router(salaries.router)
subapi.include_router(payroll.router)
subapi.include_router(attendance.router)
subapi.include_router(product.router)
subapi.include_router(supplier.router)
subapi.include_router(community_msg.router)
subapi.include_router(leaves.router)
subapi.include_router(members.router)
subapi.include_router(membership_plans.router)

# dashboard endpoint
# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def home()

