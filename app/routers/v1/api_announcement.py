from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_sqlalchemy import db
from app.models.models_announcement import GETAnnouncementResponse, POSTAnnouncementResponse, POSTAnnouncement
from app.models.sql_announcement import AnnouncementModel
import time

router = APIRouter()

@cbv(router)
class APIAnnouncement:

    @router.get("/", response_model=GETAnnouncementResponse, summary="Query all announcements for project")
    async def get_announcements(self, project_code: str, version: str = ""):
        api_response = GETAnnouncementResponse()
        query_data = {
            "project_code": project_code,
        }
        if version:
            query_data["version"] = version
        announcements = db.session.query(AnnouncementModel).filter_by(**query_data).all()
        results = []
        for announcement in announcements:
            results.append(announcement.to_dict())
        api_response.result = results
        return api_response.json_response()

    @router.post("/", response_model=POSTAnnouncementResponse, summary="Create new announcement")
    async def create_announcement(self, data: POSTAnnouncement):
        api_response = POSTAnnouncementResponse()

        if len(data.content) > 250:
            api_response.set_error_msg("Content to long")
            api_response.code = EAPIResponseCode.bad_request
            return api_response.to_dict, api_response.code

        model_data = {
            "project_code": data.project_code,
            "version": str(time.time()),
            "content": data.content,
            "publisher": data.publisher,
        }
        announcement = AnnouncementModel(**model_data)
        try:
            db.session.add(announcement)
            db.session.commit()
            db.session.refresh(announcement)
        except sqlalchemy.exc.IntegrityError as e:
            api_response.set_error_msg("project_code and version already exist in db")
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.to_dict, api_response.code
        api_response.result = announcement.to_dict()
        return api_response.json_response()



