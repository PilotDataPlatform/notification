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

import time

from fastapi import APIRouter
from fastapi import Depends
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError

from app.models.base_models import EAPIResponseCode
from app.models.models_announcement import GETAnnouncement
from app.models.models_announcement import GETAnnouncementResponse
from app.models.models_announcement import POSTAnnouncement
from app.models.models_announcement import POSTAnnouncementResponse
from app.models.sql_announcement import AnnouncementModel
from app.routers.v1.router_utils import paginate

router = APIRouter()


@cbv(router)
class APIAnnouncement:
    @router.get(
        '/',
        response_model=GETAnnouncementResponse,
        summary='Query all announcements for project')
    async def get_announcements(
        self,
        params: GETAnnouncement = Depends(GETAnnouncement)
    ):
        api_response = GETAnnouncementResponse()
        no_enddate = params.start_date and not params.end_date
        no_startdate = params.end_date and not params.start_date
        if no_enddate or no_startdate:
            api_response.error_msg = (
                'Both start_date and end_date '
                'need to be supplied')
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        query_data = {
            'project_code': params.project_code,
        }
        if params.version:
            query_data['version'] = params.version

        if params.sorting:
            if params.order == 'asc':
                sort_param = getattr(AnnouncementModel, params.sorting).asc()
            else:
                sort_param = getattr(AnnouncementModel, params.sorting).desc()
            announcements = db.session.query(AnnouncementModel).filter_by(
                **query_data).order_by(sort_param)
        else:
            sort_param = getattr(AnnouncementModel, params.sorting).asc()
            announcements = db.session.query(AnnouncementModel).filter_by(
                **query_data).order_by(sort_param)

        if params.start_date and params.end_date:
            announcements = announcements.filter(
                AnnouncementModel.date >= params.start_date,
                AnnouncementModel.date <= params.end_date
            )
        paginate(params, api_response, announcements)
        return api_response.json_response()

    @router.post(
        '/',
        response_model=POSTAnnouncementResponse,
        summary='Create new announcement')
    async def create_announcement(self, data: POSTAnnouncement):
        api_response = POSTAnnouncementResponse()

        if len(data.content) > 250:
            api_response.error_msg = 'Content to long'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        model_data = {
            'project_code': data.project_code,
            'version': str(time.time()),
            'content': data.content,
            'publisher': data.publisher,
        }
        announcement = AnnouncementModel(**model_data)
        try:
            db.session.add(announcement)
            db.session.commit()
            db.session.refresh(announcement)
        except IntegrityError:
            api_response.set_error_msg(
                'project_code and version already exist in db')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.to_dict, api_response.code
        api_response.result = announcement.to_dict()
        return api_response.json_response()
