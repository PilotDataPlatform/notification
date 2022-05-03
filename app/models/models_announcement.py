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

from pydantic import BaseModel
from pydantic import Field

from .base_models import APIResponse
from .base_models import PaginationRequest


class GETAnnouncementResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {'content': 'Hello World Again!', 'id': 1, 'project_code': 'hello', 'version': '2.0'},
        },
    )


class GETAnnouncement(PaginationRequest):
    project_code: str
    start_date: str = Field('', example='2021-02-23')
    end_date: str = Field('', example='2021-02-23')
    version: str = ''
    page_size: int = 10
    sorting: str = 'version'


class POSTAnnouncementResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {'content': 'Hello World Again!', 'id': 1, 'project_code': 'hello', 'version': '2.0'},
        },
    )


class POSTAnnouncement(BaseModel):
    project_code: str
    content: str
    publisher: str
