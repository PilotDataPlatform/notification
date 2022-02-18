"""Add unsubscribed_notifications table

Revision ID: acfc65939c91
Revises: f7b7903f78c4
Create Date: 2022-01-21 11:54:15.802511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acfc65939c91'
down_revision = 'f7b7903f78c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('unsubscribed_notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('notification_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='notifications'
    )

def downgrade():
    op.drop_table('unsubscribed_notifications', schema='notifications')
