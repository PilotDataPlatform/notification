# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Add unsubscribed_notifications table.

Revision ID: acfc65939c91
Revises: f7b7903f78c4
Create Date: 2022-01-21 11:54:15.802511
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'acfc65939c91'
down_revision = 'f7b7903f78c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'unsubscribed_notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('notification_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='notifications',
    )


def downgrade():
    op.drop_table('unsubscribed_notifications', schema='notifications')
