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
    op.add_column(
        'system_maintenance',
        sa.Column('created_date', sa.DateTime(), nullable=True),
        schema='notifications')


def downgrade():
    op.drop_column(
        'system_maintenance', 'created_date', schema='notifications')
