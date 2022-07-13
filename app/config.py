from functools import lru_cache
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

from common import VaultClient
from pydantic import BaseSettings
from pydantic import Extra


class VaultConfig(BaseSettings):
    """Store vault related configuration."""

    APP_NAME: str = 'service_notification'
    CONFIG_CENTER_ENABLED: bool = False

    VAULT_URL: Optional[str]
    VAULT_CRT: Optional[str]
    VAULT_TOKEN: Optional[str]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    config = VaultConfig()

    if not config.CONFIG_CENTER_ENABLED:
        return {}

    client = VaultClient(
        config.VAULT_URL,
        config.VAULT_CRT,
        config.VAULT_TOKEN)
    return client.get_from_vault(config.APP_NAME)


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
    POSTFIX_URL: str = 'mailhog'
    POSTFIX_PORT: str = '1025'
    ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    IMAGE_EXTENSIONS: Set[str] = {'png', 'jpg', 'jpeg', 'gif'}
    RDS_HOST: str = 'db'
    RDS_PORT: str = '5432'
    RDS_USER: str = 'postgres'
    RDS_PWD: str = 'postgres'
    NOTIFICATIONS_DBNAME: str = 'notifications'
    NOTIFICATIONS_SCHEMA: str = 'notifications'
    ANNOUNCEMENTS_SCHEMA: str = 'announcements'
    version = '1.1.0'
    api_modules = API_MODULES

    def __init__(self):
        super().__init__()
        url = (
            f'postgresql+asyncpg://{self.RDS_USER}:{self.RDS_PWD}'
            f'@{self.RDS_HOST}/{self.NOTIFICATIONS_DBNAME}')
        self.SQLALCHEMY_DATABASE_URI = (url)
        if self.postfix != '' and self.smtp_port:
            self.POSTFIX_URL = self.postfix
            self.POSTFIX_PORT = self.smtp_port

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings
        ):
            return (
                env_settings,
                load_vault_settings,
                init_settings,
                file_secret_settings)


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
