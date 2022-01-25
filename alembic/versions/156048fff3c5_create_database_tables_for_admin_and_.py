"""create database tables for admin and employee side of things

Revision ID: 156048fff3c5
Revises: 
Create Date: 2022-01-20 23:50:31.978372

"""
from itertools import product
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text



# revision identifiers, used by Alembic.
revision = '156048fff3c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('user_id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('email_id',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )

    op.create_table('salary',
    sa.Column('salary_id',sa.Integer(),nullable=True,primary_key=True),
    sa.Column('emp_type',sa.Enum('full time', 'part time', 'contract',name="emp_type_enum", create_type=False),nullable=False),
    sa.Column('salary',sa.DECIMAL(8,2),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_table('employees',
    sa.Column('employee_id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('user_id',sa.Integer(),nullable=False),
    sa.Column('salary_id',sa.Integer(),nullable=False),
    sa.Column('first_name',sa.String(),nullable=False),
    sa.Column('last_name',sa.String(),nullable=False),
    sa.Column('date_of_birth',sa.DATE(),nullable=False),
    sa.Column('address',sa.String(),nullable=False),
    sa.Column('state',sa.String(),nullable=False),
    sa.Column('zip_code',sa.String(6),nullable=False),
    sa.Column('primary_phone',sa.String(10),nullable=False),
    sa.Column('additional_phone',sa.String(10),nullable=False),
    sa.Column('emergency_contact_name',sa.String(),nullable=False),
    sa.Column('emergency_contact_phone',sa.String(10),nullable=False),
    sa.Column('photograph',sa.String(),nullable=False),
    sa.Column('aadhar_no',sa.String(13),nullable=False),
    sa.Column('pan_no',sa.String(10),nullable=False),
    sa.Column('designation',sa.Enum('admin','trainer','receptionist',name="designation_enum", create_type=False),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('emp_users_fk',source_table='employees',referent_table='users',local_cols=['user_id'],remote_cols=['user_id'],ondelete='CASCADE')
    op.create_foreign_key('emp_sal_fk',source_table='employees',referent_table='salary',local_cols=['salary_id'],remote_cols=['salary_id'],ondelete='CASCADE')

    
    op.create_table('payroll',
    sa.Column('payroll_id',sa.Integer(),nullable=True,primary_key=True),
    sa.Column('employee_id',sa.Integer(),nullable=False),
    sa.Column('account_id',sa.BigInteger,nullable=False),
    sa.Column('transaction_id',sa.String(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('emp_payroll_fk',source_table='payroll',referent_table='employees',local_cols=['employee_id'],remote_cols=['employee_id'],ondelete='CASCADE')
    
    op.create_table('leave',
    sa.Column('leave_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('leave_title',sa.Integer(),nullable=False),
    sa.Column('employee_id',sa.Integer(),nullable=False),
    sa.Column('applied_for',sa.DATE(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('emp_leave_fk',source_table='leave',referent_table='employees',local_cols=['employee_id'],remote_cols=['employee_id'],ondelete='CASCADE')

    op.create_table('employee_attendance',
    sa.Column('attendance_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('employee_id',sa.Integer(),nullable=False),
    sa.Column('check_in_time',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    sa.Column('check_out_time',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    )
    op.create_foreign_key('emp_attendance_fk',source_table='employee_attendance',referent_table='employees',local_cols=['employee_id'],remote_cols=['employee_id'],ondelete='CASCADE')

    op.create_table('supplier',
    sa.Column('supplier_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('supplier_name',sa.String(),nullable=False),
    sa.Column('supplier_phone',sa.String(10),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )

    op.create_table('product',
    sa.Column('product_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('supplier_id',sa.Integer(),nullable=False),
    sa.Column('product_title',sa.String(),nullable=False),
    sa.Column('product_description',sa.Text(),nullable=False),
    sa.Column('quantity',sa.Integer(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('product_supplier_fk',source_table='product',referent_table='supplier',local_cols=['supplier_id'],remote_cols=['supplier_id'],ondelete='CASCADE')

    op.create_table('community_message',
    sa.Column('message_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('message_title',sa.String(),nullable=False),
    sa.Column('message_description',sa.Text,nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )

    pass


def downgrade():
    op.drop_table('users')
    op.drop_table('employees')
    op.drop_table('salary')
    op.drop_table('payroll')
    op.drop_table('leave')
    op.drop_table('employee_attendance')
    op.drop_table('supplier')
    op.drop_table('product')
    op.drop_table('community_message')

    pass
