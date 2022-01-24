from fastapi_sqlalchemy import db 
from sqlalchemy import Column, String, DateTime, Integer, Column, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.config import ConfigClass

Base = declarative_base()


class AnnouncementModel(Base):
    __tablename__ = 'announcement'
    id = Column(Integer, unique=True, primary_key=True)
    project_code = Column(String())
    content = Column(String())
    version = Column(String())
    publisher = Column(String())
    date = Column(DateTime(), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('project_code', 'version', name='project_code_version'),
        {"schema": ConfigClass.RDS_SCHEMA_DEFAULT},
    )

    def __init__(self, project_code, content, version, publisher):
        self.project_code = project_code
        self.content = content
        self.version = version
        self.publisher = publisher

    def to_dict(self):
        result = {}
        for field in ["id", "project_code", "content", "version", "date", "publisher"]:
            if field == "date":
                result[field] = str(getattr(self, field))
            else:
                result[field] = getattr(self, field)

        return result


class NotificationModel(Base):
    __tablename__ = 'system_maintenance'
    id = Column(Integer, unique=True, primary_key=True)
    type = Column(String())
    message = Column(String())
    maintenance_date = Column(DateTime())
    duration = Column(Integer())
    duration_unit = Column(String())

    __table_args__ = (
        {"schema": ConfigClass.RDS_SCHEMA_DEFAULT},
    )

    def __init__(self, type, message, maintenance_date, duration, duration_unit):
        self.type = type
        self.message = message
        self.maintenance_date = maintenance_date
        self.duration = duration
        self.duration_unit = duration_unit

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'message': self.message,
            'detail': {
                'maintenance_date': str(self.maintenance_date),
                'duration': self.duration,
                'duration_unit': self.duration_unit
            }
        }


class UnsubscribedModel(Base):
    __tablename__ = 'unsubscribed_notifications'
    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String())
    notification_id = Column(Integer())

    __table_args__ = (
        {"schema": ConfigClass.RDS_SCHEMA_DEFAULT},
    )

    def __init__(self, username, notification_id):
        self.username = username
        self.notification_id = notification_id

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'notification_id': self.notification_id
        }
