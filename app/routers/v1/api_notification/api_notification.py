from fastapi import APIRouter
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from app.models.base_models import EAPIResponseCode
from app.models.models_notification import POSTNotification
from app.models.models_notification import POSTNotificationResponse
from app.models.sql_announcement import NotificationModel

router = APIRouter()


@cbv(router)
class APIAnnouncement:
    @router.post("/", response_model=POSTNotificationResponse, summary="Create new maintenance notification")
    async def create_notification(self, data: POSTNotification):
        api_response = POSTNotificationResponse()
        if len(data.message) > 250:
            api_response.set_error_msg("Message too long")
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        model_data = {
            'type': data.type,
            'message': data.message,
            'maintenance_date': data.detail.maintenance_date,
            'duration': data.detail.duration,
            'duration_unit': data.detail.duration_unit,
        }
        notification = NotificationModel(**model_data)
        try:
            db.session.add(notification)
            db.session.commit()
            db.session.refresh(notification)
        except Exception as e:
            print(e)
            api_response.set_error_msg("Failed to write to database")
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        api_response.result = notification.to_dict()
        return api_response.json_response()
