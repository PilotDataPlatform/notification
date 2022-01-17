from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from app.models.base_models import EAPIResponseCode
from app.models.models_notification import POSTNotification, POSTNotificationResponse, GETNotifications, GETNotificationResponse
from app.models.sql_announcement import NotificationModel
from app.routers.v1.router_utils import paginate

router = APIRouter()
routerBulk = APIRouter()


@cbv(router)
class APINotification:
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

@cbv(routerBulk)
class APINotificationBulk:
    @routerBulk.get("/", response_model=GETNotificationResponse, summary="Query many maintenance notifications")
    async def get_all_notifications(self, params: GETNotifications = Depends(GETNotifications)):
        api_response = GETNotificationResponse()
        notifications = db.session.query(NotificationModel)
        paginate(params, api_response, notifications)
        return api_response.json_response()
