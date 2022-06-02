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
from datetime import timezone

from common import LoggerFactory
from fastapi import APIRouter
from fastapi import Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.dependencies.db import get_db_session
from app.models.base_models import EAPIResponseCode
from app.models.models_notification import DELETENotification
from app.models.models_notification import DELETENotificationResponse
from app.models.models_notification import GETNotification
from app.models.models_notification import GETNotificationResponse
from app.models.models_notification import GETNotifications
from app.models.models_notification import POSTNotification
from app.models.models_notification import POSTNotificationResponse
from app.models.models_notification import PUTNotification
from app.models.models_notification import PUTNotificationParams
from app.models.models_notification import PUTNotificationResponse
from app.models.models_unsub import POSTUnsub
from app.models.models_unsub import POSTUnsubResponse
from app.models.sql_notification import NotificationModel
from app.models.sql_notification import UnsubscribedModel
from app.routers.v1.router_utils import paginate

router = APIRouter()
routerBulk = APIRouter()
routerUnsub = APIRouter()
_logger = LoggerFactory('api_notification').get_logger()


@cbv(router)
class APINotification:
    @router.get(
        '/',
        response_model=GETNotificationResponse,
        summary='Query one maintenance notification by ID')
    async def get_notification(
            self, db: AsyncSession = Depends(get_db_session), params: GETNotification = Depends(GETNotification)
    ):
        try:
            api_response = GETNotificationResponse()
            query = select(NotificationModel).filter_by(id=params.id)
            notification = (await db.execute(query)).scalars().first()
            api_response.page = 0
            api_response.num_of_pages = 1
            api_response.total = 1
            api_response.result = notification.to_dict()
        except Exception as e:
            readable_error = f'Could not get notification with id={params.id}'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()

    @router.post(
        '/',
        response_model=POSTNotificationResponse,
        summary='Create new maintenance notification')
    async def create_notification(self, data: POSTNotification, db: AsyncSession = Depends(get_db_session)):
        api_response = POSTNotificationResponse()
        if len(data.message) > 250:
            api_response.set_error_msg('Message too long')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        if int(data.detail.duration) <= 0:
            api_response.set_error_msg('Duration less than or equal to zero')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        model_data = {
            'notification_type': data.type,
            'message': data.message,
            'maintenance_date': data.detail.maintenance_date.replace(tzinfo=None),
            'duration': data.detail.duration,
            'duration_unit': data.detail.duration_unit,
            'created_date': datetime.now(timezone.utc).replace(tzinfo=None),
        }
        notification = NotificationModel(**model_data)
        try:
            db.add(notification)
            await db.commit()
            await db.refresh(notification)
            api_response.result = notification.to_dict()
        except Exception as e:
            readable_error = 'Failed to write to database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()

    @router.put(
        '/',
        response_model=PUTNotificationResponse,
        summary='Modify one maintenance notification by ID')
    async def modify_notification(
            self,
            data: PUTNotification,
            db: AsyncSession = Depends(get_db_session),
            params: PUTNotificationParams = Depends(PUTNotificationParams)
    ):
        api_response = PUTNotificationResponse()
        if len(data.message) > 250:
            api_response.set_error_msg('Message too long')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        if int(data.detail.duration) <= 0:
            api_response.set_error_msg('Duration less than or equal to zero')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        try:
            notification_id = params.id
            query = select(NotificationModel).filter_by(id=notification_id)
            notification = (await db.execute(query)).scalars().first()
            notification.type = data.type
            notification.message = data.message
            notification.created_date = datetime.now(timezone.utc).replace(tzinfo=None)
            notification.maintenance_date = data.detail.maintenance_date.replace(tzinfo=None)
            notification.duration = data.detail.duration
            notification.duration_unit = data.detail.duration_unit
            await db.commit()
            await db.refresh(notification)
            api_response.result = notification.to_dict()
        except Exception as e:
            readable_error = 'Failed to write to database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()

    @router.delete(
        '/',
        response_model=DELETENotificationResponse,
        summary='Delete one maintenance notification by ID')
    async def delete_notification(
            self, params: DELETENotification = Depends(DELETENotification),
            db: AsyncSession = Depends(get_db_session)
    ):
        api_response = DELETENotificationResponse()
        try:
            query = select(NotificationModel).filter_by(id=params.id)
            notification = (await db.execute(query)).scalars().first()
            await db.delete(notification)
            await db.commit()
        except Exception as e:
            readable_error = 'Failed to delete from database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()


@cbv(routerBulk)
class APINotificationBulk:
    @routerBulk.get(
        '/',
        response_model=GETNotificationResponse,
        summary='Query many maintenance notifications')
    async def get_all_notifications(
            self, params: GETNotifications = Depends(GETNotifications),
            db: AsyncSession = Depends(get_db_session)
    ):
        api_response = GETNotificationResponse()
        query = select(NotificationModel).order_by(NotificationModel.created_date.desc())
        if not params.all:
            if not params.username:
                api_response.error_msg = (
                    'Username must be provided '
                    'if all is false')
                api_response.code = EAPIResponseCode.bad_request
                return api_response.json_response()
            unsubscribe_query = select(UnsubscribedModel).filter_by(
                username=params.username)
            unsubs = (await db.execute(unsubscribe_query)).scalars().all()
            unsubNotificationIds = []
            for unsub in unsubs:
                unsubNotificationIds.append(unsub.notification_id)
            query = query.filter(
                NotificationModel.id.not_in(unsubNotificationIds))
        await paginate(params, api_response, query, db)
        return api_response.json_response()


@cbv(routerUnsub)
class APINotificationUnsub:
    @routerUnsub.post(
        '/',
        response_model=POSTUnsubResponse,
        summary='Unsubscribe one user from one maintenance notification'
    )
    async def unsub_notification(self, data: POSTUnsub, db: AsyncSession = Depends(get_db_session)):
        api_response = POSTUnsubResponse()
        model_data = {
            'username': data.username,
            'notification_id': data.notification_id}
        unsub = UnsubscribedModel(**model_data)
        try:
            db.add(unsub)
            await db.commit()
            await db.refresh(unsub)
            api_response.result = unsub.to_dict()
        except Exception as e:
            readable_error = 'Failed to write to database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()
