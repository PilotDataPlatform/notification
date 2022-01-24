from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from app.config import ConfigClass

Base = declarative_base()


class NotificationModel(Base):
    __tablename__ = 'system_maintenance'
    id = Column(Integer, unique=True, primary_key=True)
    type = Column(String())
    message = Column(String())
    maintenance_date = Column(DateTime())
    duration = Column(Integer())
    duration_unit = Column(String())
    created_date = Column(DateTime())

    __table_args__ = (
        {"schema": ConfigClass.RDS_SCHEMA_DEFAULT},
    )

    def __init__(self, type, message, maintenance_date, duration, duration_unit, created_date):
        self.type = type
        self.message = message
        self.maintenance_date = maintenance_date
        self.duration = duration
        self.duration_unit = duration_unit
        self.created_date = created_date

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'message': self.message,
            'created_date': str(self.created_date),
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
