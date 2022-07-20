from common import LoggerFactory
from app.models.sql_notification import NotificationModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db_session
from fastapi import Depends
from sqlalchemy.sql import select
from app.models.sql_announcement import AnnouncementModel

_logger = LoggerFactory('api_health').get_logger()


async def opsdb_check(db: AsyncSession = Depends(get_db_session)):
    try:
        query = select(AnnouncementModel)
        (await db.execute(query)).scalars().first()
    except Exception as e:
        _logger.error(f'Could not connect to notifications.announcement table: {e}')
        return False

    try:
        query = select(NotificationModel)
        (await db.execute(query)).scalars().first()
    except Exception as e:
        _logger.error(f'Could not connect to notifications.system_maintenance table: {e}')
        return False

    return True
