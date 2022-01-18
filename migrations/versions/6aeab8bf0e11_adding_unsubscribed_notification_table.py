"""Adding unsubscribed_notification table

Revision ID: 6aeab8bf0e11
Revises: 3518d7f9f853
Create Date: 2022-01-18 11:20:49.105552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aeab8bf0e11'
down_revision = '3518d7f9f853'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('unsubscribed_notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('notification_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='indoc_vre'
    )

def downgrade():
    op.drop_table('unsubscribed_notification', schema='indoc_vre')
