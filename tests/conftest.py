import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateSchema, CreateTable
from sqlalchemy_utils import create_database, database_exists
from testcontainers.postgres import PostgresContainer

from app.main import create_app
from app.config import ConfigClass
from app.models.sql_notification import NotificationModel
from app.models.sql_announcement import AnnouncementModel


@pytest.fixture(scope='session', autouse=True)
def db():
    with PostgresContainer('postgres:14.1') as postgres:
        postgres_uri = postgres.get_connection_url()
        if not database_exists(postgres_uri):
            create_database(postgres_uri)
        engine = create_engine(postgres_uri)

        from app.models.sql_notification import Base
        CreateTable(NotificationModel.__table__).compile(dialect=postgresql.dialect())
        if not engine.dialect.has_schema(engine, ConfigClass.NOTIFICATIONS_SCHEMA):
            engine.execute(CreateSchema(ConfigClass.NOTIFICATIONS_SCHEMA))
        Base.metadata.create_all(bind=engine)

        from app.models.sql_announcement import Base
        CreateTable(AnnouncementModel.__table__).compile(dialect=postgresql.dialect())
        if not engine.dialect.has_schema(engine, ConfigClass.ANNOUNCEMENTS_SCHEMA):
            engine.execute(CreateSchema(ConfigClass.ANNOUNCEMENTS_SCHEMA))
        Base.metadata.create_all(bind=engine)
        yield postgres


@pytest.fixture
def test_client(db):
    ConfigClass.SQLALCHEMY_DATABASE_URI = db.get_connection_url()
    app = create_app()
    client = TestClient(app)
    return client
