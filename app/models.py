from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,Enum,DECIMAL,Text,DATE, null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger
from .database import Base
from sqlalchemy.sql.expression import text

class Users(Base):
    __tablename__="users"

    user_id=Column(Integer,primary_key=True, nullable=False)
    email_id=Column(String(255),unique=True,nullable=False)
    password=Column(String(255),nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Employee(Base):
    __tablename__="employees"

    employee_id=Column(Integer, primary_key=True, nullable=False)
    user_id=Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    salary_id=Column(Integer,ForeignKey("salary.salary_id",ondelete="CASCADE"),nullable=False)
    first_name=Column(String(255),nullable=False)
    last_name=Column(String(255),nullable=False)
    date_of_birth=Column(DATE,nullable=False)
    address=Column(String(255),nullable=False)
    state=Column(String(255),nullable=False)
    zip_code=Column(String(6),nullable=False)
    primary_phone=Column(String(10),nullable=False,unique=True)
    additional_phone=Column(String(10),nullable=True,default="na")
    emergency_contact_name=Column(String(255),nullable=False)
    emergency_contact_phone=Column(String(255),nullable=False)
    photograph=Column(String(255),nullable=False,default="app\images\default.png")
    aadhar_no=Column(String(13),nullable=False,unique=True)
    pan_no=Column(String(10),nullable=False,unique=True)
    designation=Column(Enum("admin","trainer","receptionist",name="designation_enum", create_type=False),nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
class Salary(Base):
    __tablename__="salary"

    salary_id=Column(Integer, primary_key=True, nullable=False)
    emp_type=Column(Enum("full time", "part time", "contract",name="emp_type_enum", create_type=False),nullable=False)
    salary=Column(DECIMAL(8,2),nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Payroll(Base):
    __tablename__="payroll"

    payroll_id=Column(Integer,primary_key=True,nullable=False)
    emp_id=Column(Integer,ForeignKey("employees.employee_id",ondelete="CASCADE"),nullable=False)
    account_id=Column(BigInteger,nullable=False)
    transaction_id=Column(String(255),nullable=False,unique=True)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Leaves(Base):
    __tablename__="leave"

    leave_id=Column(Integer, primary_key=True, nullable=False)
    leave_title=Column(String(255),nullable=False)
    emp_id=Column(Integer,ForeignKey("employees.employee_id",ondelete="CASCADE"),nullable=False)
    leave_message=Column(Text,nullable=False)
    applied_for=Column(DATE,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class EmployeeAttendance(Base):
    __tablename__="employee_attendance"

    attendance_id=Column(Integer,primary_key=True, nullable=False)
    emp_id=Column(Integer,ForeignKey("employees.employee_id",ondelete="CASCADE"),nullable=False)
    check_in_time=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    check_out_time=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

#add the supplier model
class Supplier(Base):
    __tablename__= "supplier"

    supplier_id=Column(Integer,primary_key=True, nullable=False)
    supplier_name=Column(String(255),nullable=False)
    supplier_phone=Column(String(255),nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Product(Base):
    __tablename__="product"

    product_id=Column(Integer,primary_key=True, nullable=False)
    sup_id=Column(Integer,ForeignKey("supplier.supplier_id",ondelete="CASCADE"),nullable=False)
    prodct_title=Column(String(255),nullable=False)
    product_description=Column(Text,nullable=False)
    product_price=Column(DECIMAL(10,2),nullable=False)
    product_img=Column(String(),nullable=False,default='app\images\default.png')
    quantity=Column(Integer,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class CommunityMessage(Base):
    __tablename__="community_message"

    message_id=Column(Integer,primary_key=True, nullable=False)
    message_title=Column(String(255),nullable=False)
    message_description=Column(Text,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class OrderItem(Base):
    __tablename__="order_item"

    item_id=Column(Integer,primary_key=True,nullable=False)
    product_title=Column(String(255),nullable=False)
    product_id=Column(Integer,ForeignKey("product.product_id",ondelete="CASCADE"),nullable=False)
    product_description=Column(Text,nullable=False)
    product_price=Column(DECIMAL(10,2),nullable=False)
    quantity=Column(Integer,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Order(Base):
    __tablename__="order"

    order_id=Column(Integer,primary_key=True,nullable=False)
    order_date=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id=Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    amount=Column(DECIMAL(10,2),nullable=False)
    payment_mode=Column(String(255),nullable=False)
    quantity=Column(Integer,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Payments(Base):
    __tablename__="payments"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(255),nullable=False)
    user_id=Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    contact=Column(String(10),nullable=False)
    email_id=Column(String(255),nullable=False)
    transaction_id=Column(String(255),nullable=False)
    invoice_no=Column(String(255),nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class MembershipPlans(Base):
    __tablename__="membership_plans"

    plan_id=Column(Integer,primary_key=True,nullable=False)
    plan_name=Column(String(255),nullable=False)
    plan_description=Column(Text,nullable=False)
    plan_validity=Column(Integer,nullable=False)
    plan_price=Column(DECIMAL(6,2),nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Members(Base):
    __tablename__="members"

    member_id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey("user.user_id",ondelete="CASCADE"),nullable=False)
    first_name=Column(String(255),nullable=False)
    last_name=Column(String(255),nullable=False)
    date_of_birth=Column(DATE,nullable=False)
    address=Column(String(255),nullable=False)
    state=Column(String(255),nullable=False)
    zip_code=Column(String(6),nullable=False)
    primary_phone=Column(String(10),nullable=False,unique=True)
    additional_phone=Column(String(10),nullable=True,default="na")
    emergency_contact_name=Column(String(255),nullable=False)
    emergency_contact_phone=Column(String(255),nullable=False)
    photograph=Column(String(255),nullable=False,default="app\images\default.png")
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
class MembershipSubscription(Base):
    __tablename__="membership_subscription"

    subscription_id=Column(Integer,primary_key=True,nullable=False)
    plan_name=Column(String(255),nullable=False)
    member_id=Column(Integer,ForeignKey("members.member_id",ondelete="CASCADE"),nullable=False)
    plan_id=Column(Integer,ForeignKey("membership_plans.plan_id",ondelete="CASCADE"),nullable=False)
    plan_description=Column(String(255),nullable=False)
    plan_validity=Column(Integer,nullable=False)
    plan_price=Column(DECIMAL(6,2),nullable=False)
    plan_start_date=Column(DATE,nullable=False)
    plan_end_date=Column(DATE,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
