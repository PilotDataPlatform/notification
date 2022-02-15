from functools import lru_cache
from typing import Any
from typing import Dict
from typing import List
from typing import Set

from common import VaultClient
from pydantic import BaseSettings
from pydantic import Extra
from starlette.config import Config

config = Config('.env')
SRV_NAMESPACE = config('APP_NAME', cast=str, default='service_notification')
CONFIG_CENTER_ENABLED = config('CONFIG_CENTER_ENABLED', cast=str, default='false')


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    if CONFIG_CENTER_ENABLED == 'false':
        return {}
    else:
        return vault_factory()


def vault_factory() -> dict:
    vc = VaultClient(config('VAULT_URL'), config('VAULT_CRT'), config('VAULT_TOKEN'))
    return vc.get_from_vault(SRV_NAMESPACE)


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'service_notification'
    port: int = 5065
    host: str = '0.0.0.0'
    namespace: str = ''
    env: str = 'test'
    OPEN_TELEMETRY_ENABLED: bool = False
    API_MODULES: List = ['service_email']
    postfix: str = ''
    smtp_user: str = ''
    smtp_pass: str = ''
    smtp_port: str = ''
    POSTFIX_URL: str
    POSTFIX_PORT: str
    ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    IMAGE_EXTENSIONS: Set[str] = {'png', 'jpg', 'jpeg', 'gif'}
    RDS_HOST: str
    RDS_PORT: str
    RDS_USER: str
    RDS_PWD: str
    NOTIFICATIONS_DBNAME: str = 'notifications'
    NOTIFICATIONS_SCHEMA: str = 'notifications'
    ANNOUNCEMENTS_SCHEMA: str = 'announcements'
    version = '1.1.0'
    api_modules = API_MODULES
    TEST_EMAIL_SENDER: str = 'sender@test.com'
    TEST_EMAIL_RECEIVER: str = 'receiver@test.com'
    TEST_EMAIL_RECEIVER_2: str = 'receiver2@test.com'

    def __init__(self):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = (
            f'postgresql://{self.RDS_USER}:{self.RDS_PWD}@{self.RDS_HOST}/{self.NOTIFICATIONS_DBNAME}'
        )
        if self.postfix != '' and self.smtp_port:
            self.POSTFIX_URL = self.postfix
            self.POSTFIX_PORT = self.smtp_port

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return load_vault_settings, env_settings, init_settings, file_secret_settings


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
