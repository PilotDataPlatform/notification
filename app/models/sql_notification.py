from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
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

    __table_args__ = ({'schema': ConfigClass.NOTIFICATIONS_SCHEMA},)

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
            'created_date': self.created_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'detail': {
                'maintenance_date': self.maintenance_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'duration': self.duration,
                'duration_unit': self.duration_unit,
            },
        }


class UnsubscribedModel(Base):
    __tablename__ = 'unsubscribed_notifications'
    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String())
    notification_id = Column(Integer())

    __table_args__ = ({'schema': ConfigClass.NOTIFICATIONS_SCHEMA},)

    def __init__(self, username, notification_id):
        self.username = username
        self.notification_id = notification_id

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'notification_id': self.notification_id}
