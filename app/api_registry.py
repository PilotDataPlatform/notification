from fastapi import FastAPI
from .routers.v1 import api_announcement
from .routers.v1.api_email import api_email

def api_registry(app: FastAPI):
    app.include_router(api_announcement.router, prefix="/v1/announcements")
    app.include_router(api_email.router, prefix="/v1/email")