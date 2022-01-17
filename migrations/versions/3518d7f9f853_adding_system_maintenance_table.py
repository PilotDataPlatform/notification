"""Adding system_maintenance table

Revision ID: 3518d7f9f853
Revises: 19c5300a4b2f
Create Date: 2022-01-17 13:41:58.410491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3518d7f9f853'
down_revision = '19c5300a4b2f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('system_maintenance',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('maintenance_date', sa.DateTime(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('duration_unit', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        schema='indoc_vre'
    )

def downgrade():
    op.drop_table('system_maintenance', schema='indoc_vre')
