"""creating all database tables

Revision ID: 8168df2384a0
Revises: 156048fff3c5
Create Date: 2022-02-20 23:01:44.563682

"""
from sqlalchemy.sql.expression import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8168df2384a0'
down_revision = '156048fff3c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('order_item',
    sa.Column('item_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('product_id',sa.Integer(),nullable=False),
    sa.Column('product_title',sa.String(),nullable=False),
    sa.Column('product_description',sa.Text(),nullable=False),
    sa.Column('product_price',sa.DECIMAL(10,2),nullable=False),
    sa.Column('quantity',sa.Integer(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )      
    op.create_foreign_key('order_item_product_fk',source_table='order_item',referent_table='product',local_cols=['product_id'],remote_cols=['product_id'],ondelete='CASCADE')

    op.create_table('order',
    sa.Column('order_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('user_id',sa.Integer(),nullable=False),
    sa.Column('amount',sa.DECIMAL(10,2),nullable=False),
    sa.Column('payment_mode',sa.String(),nullable=False),
    sa.Column('quantity',sa.Integer(),nullable=False),
    sa.Column('order_time',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('order_user_fk',source_table='order',referent_table='users',local_cols=['user_id'],remote_cols=['user_id'],ondelete='CASCADE')

    op.create_table('payments',
    sa.Column('id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('name',sa.String(),nullable=False),
    sa.Column('user_id',sa.Integer(),nullable=False),
    sa.Column('contact',sa.String(10),nullable=False),
    sa.Column('email_id',sa.String(),nullable=False),
    sa.Column('transaction_id',sa.String(),nullable=False),
    sa.Column('invoice_no',sa.String(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('payment_user_fk',source_table='payments',referent_table='users',local_cols=['user_id'],remote_cols=['user_id'],ondelete='CASCADE')

    op.create_table('membership_plans',
    sa.Column('plan_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('plan_name',sa.String(),nullable=False),
    sa.Column('plan_description',sa.Text(),nullable=False),
    sa.Column('plan_validity',sa.Integer(),nullable=False),
    sa.Column('plan_price',sa.DECIMAL(6,2),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    
    op.create_table('members',
    sa.Column('member_id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('user_id',sa.Integer(),nullable=False),
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
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('member_users_fk',source_table='members',referent_table='users',local_cols=['user_id'],remote_cols=['user_id'],ondelete='CASCADE')
    
    op.create_table('membership_subscription',
    sa.Column('subscription_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('plan_name',sa.String(),nullable=False),
    sa.Column('member_id',sa.Integer(),nullable=False),
    sa.Column('plan_id',sa.Integer(),nullable=False),
    sa.Column('plan_description',sa.String(),nullable=False),
    sa.Column('plan_validity',sa.Integer(),nullable=False),
    sa.Column('plan_price',sa.DECIMAL(6,2),nullable=False),
    sa.Column('plan_start_date',sa.DATE(),nullable=False),
    sa.Column('plan_end_date',sa.DATE(),nullable=False),
    sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )
    op.create_foreign_key('subscription_member_fk',source_table='membership_subscription',referent_table='members',local_cols=['member_id'],remote_cols=['member_id'],ondelete='CASCADE')
    op.create_foreign_key('subscription_plan_fk',source_table='membership_subscription',referent_table='membership_plans',local_cols=['plan_id'],remote_cols=['plan_id'],ondelete='CASCADE')
    
    pass


def downgrade():
    pass
