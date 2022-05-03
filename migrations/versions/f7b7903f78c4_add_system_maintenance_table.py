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

"""Add system_maintenance table.

Revision ID: f7b7903f78c4
Revises:
Create Date: 2022-01-21 11:53:38.076126
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f7b7903f78c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'system_maintenance',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('maintenance_date', sa.DateTime(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('duration_unit', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        schema='notifications',
    )


def downgrade():
    op.drop_table('system_maintenance', schema='notifications')
