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

"""Add announcements table.

Revision ID: 49fbb2de7523
Revises: acfc65939c91
Create Date: 2022-01-21 12:01:11.749704
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '49fbb2de7523'
down_revision = 'acfc65939c91'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'announcement',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_code', sa.String(), nullable=True),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('publisher', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('project_code', 'version', name='project_code_version'),
        schema='announcements',
    )


def downgrade():
    op.drop_table('announcement', schema='announcements')
