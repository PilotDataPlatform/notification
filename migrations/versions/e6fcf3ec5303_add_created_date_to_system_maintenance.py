"""Add created_date to system_maintenance.

Revision ID: e6fcf3ec5303
Revises: 49fbb2de7523
Create Date: 2022-01-24 13:01:15.062858
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e6fcf3ec5303'
down_revision = '49fbb2de7523'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('system_maintenance', sa.Column('created_date', sa.DateTime(), nullable=True), schema='notifications')


def downgrade():
    op.drop_column('system_maintenance', 'created_date', schema='notifications')
