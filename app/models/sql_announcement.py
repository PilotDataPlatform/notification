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

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from app.config import ConfigClass

Base = declarative_base()


class AnnouncementModel(Base):
    __tablename__ = 'announcement'
    id = Column(Integer, unique=True, primary_key=True)
    project_code = Column(String())
    content = Column(String())
    version = Column(String())
    publisher = Column(String())
    date = Column(DateTime(), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('project_code', 'version', name='project_code_version'),
        {'schema': ConfigClass.ANNOUNCEMENTS_SCHEMA},
    )

    def __init__(self, project_code, content, version, publisher):
        self.project_code = project_code
        self.content = content
        self.version = version
        self.publisher = publisher

    def to_dict(self):
        result = {}
        for field in ['id', 'project_code', 'content', 'version', 'date', 'publisher']:
            if field == 'date':
                result[field] = str(getattr(self, field))
            else:
                result[field] = getattr(self, field)

        return result
