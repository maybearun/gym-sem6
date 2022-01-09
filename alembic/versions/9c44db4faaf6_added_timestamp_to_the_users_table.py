"""added timestamp to the users table

Revision ID: 9c44db4faaf6
Revises: 
Create Date: 2022-01-09 23:21:53.976659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c44db4faaf6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',sa.Column('timestamp',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('users','timestamp')
    pass
