from datetime import datetime
from pydantic import BaseModel, Field
from .base_models import APIResponse


# GET
class GETNotificationResponse(APIResponse):
    result: dict = Field({}, example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {
                    'type': 'maintenance',
                    'message': 'Notification response message',
                    'detail': {
                        'maintenance_date': '2022-01-01',
                        'duration': '3',
                        'duration_unit': 'h',
                }
            }
    })


class GETNotifications(BaseModel):
    all: bool = True
    page_size: int = 10
    page: int = 0


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
    result: dict = Field({}, example={
            'code': 200,
            'error_msg': '',
            'result': {
                    'id': 1,
                    'status': 'success',
            }
    })


class DELETENotification(BaseModel):
    id: int
