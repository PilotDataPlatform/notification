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

from pydantic import BaseModel
from pydantic import Field

from .base_models import APIResponse


# GET
class GETNotificationResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {
                'type': 'maintenance',
                'message': 'Notification response message',
                'created_date': '2022-01-01 12:00:00.000000',
                'detail': {
                    'maintenance_date': '2022-01-01 12:00:00.000000',
                    'duration': '3',
                    'duration_unit': 'h',
                },
            },
        },
    )


class GETNotifications(BaseModel):
    all: bool = True
    page_size: int = 10
    page: int = 0
    username: str = None


class GETNotification(BaseModel):
    id: int


# POST
class POSTNotificationResponse(GETNotificationResponse):
    pass


class POSTNotificationDetail(BaseModel):
    maintenance_date: datetime
    duration: int
    duration_unit: str


class POSTNotification(BaseModel):
    type: str
    message: str
    detail: POSTNotificationDetail


# PUT
class PUTNotificationResponse(POSTNotificationResponse):
    pass


class PUTNotification(POSTNotification):
    pass


# DELETE
class DELETENotificationResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'result': {
                'id': 1,
                'status': 'success',
            },
        },
    )


class DELETENotification(BaseModel):
    id: int
