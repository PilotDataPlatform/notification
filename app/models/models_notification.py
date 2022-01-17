from datetime import datetime
from pydantic import BaseModel, Field
from .base_models import APIResponse


class POSTNotificationResponse(APIResponse):
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


class POSTNotificationDetail(BaseModel):
    maintenance_date: datetime
    duration: int
    duration_unit: str


class POSTNotification(BaseModel):
    type: str
    message: str
    detail: POSTNotificationDetail
