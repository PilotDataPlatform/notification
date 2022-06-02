import asyncio
import socket
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from fastapi.testclient import TestClient as TestClientEmail
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.schema import CreateTable
from testcontainers.postgres import PostgresContainer

from app.config import ConfigClass
from app.main import create_app
from app.models.sql_announcement import AnnouncementModel
from app.models.sql_notification import NotificationModel
from app.models.sql_notification import UnsubscribedModel


class ProcessMocked(object):
    def __init__(self, target, args):
        self.target = target
        self.args = args

    def start(self):
        self.target(*self.args)

    def join(self):
        pass


@pytest_asyncio.fixture(scope='session', autouse=True)
async def db():
    with PostgresContainer('postgres:14.1') as postgres:
        postgres_uri = postgres.get_connection_url().replace('+psycopg2', '+asyncpg')
        engine = create_async_engine(postgres_uri)
        async with engine.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {ConfigClass.NOTIFICATIONS_SCHEMA};'))
            await connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {ConfigClass.ANNOUNCEMENTS_SCHEMA};'))
            await connection.execute(CreateTable(NotificationModel.__table__))
            await connection.execute(CreateTable(AnnouncementModel.__table__))
            await connection.execute(CreateTable(UnsubscribedModel.__table__))
        yield postgres
        await engine.dispose()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    asyncio.set_event_loop_policy(None)


@pytest_asyncio.fixture
async def test_client(db):
    ConfigClass.SQLALCHEMY_DATABASE_URI = db.get_connection_url().replace('+psycopg2', '+asyncpg')
    app = create_app()
    async with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client_email():
    app = create_app()
    client = TestClientEmail(app)
    return client


@pytest.fixture(scope='function')
def smtp_mocker(mocker) -> MagicMock:
    smtp_mocker = mocker.patch('smtplib.SMTP', autospec=True)
    return smtp_mocker


@pytest.fixture(scope='function')
def smtp_mocker_connection_error(smtp_mocker: MagicMock) -> MagicMock:
    smtp_mocker.side_effect = socket.gaierror
    return smtp_mocker


@pytest.fixture(scope='function')
def mock_multiprocessing_process(mocker):
    mocker.patch('app.routers.v1.api_email.api_email.Process', new=ProcessMocked)
