from fastapi import FastAPI
from .routers.v1.api_announcement import api_announcement
from .routers.v1.api_email import api_email
from .routers.v1.api_notification import api_notification

def api_registry(app: FastAPI):
    app.include_router(api_announcement.router, prefix="/v1/announcements", tags=["announcement"])
    app.include_router(api_email.router, prefix="/v1/email", tags=["email"])
    app.include_router(api_notification.router, prefix="/v1/notification", tags=["notification"])
    app.include_router(api_notification.routerBulk, prefix="/v1/notifications", tags=["notification"])
