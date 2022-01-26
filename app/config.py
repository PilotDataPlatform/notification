import os
from common import VaultClient
from pydantic import BaseSettings, Extra
from typing import Dict, Set, List, Any
from functools import lru_cache

SRV_NAMESPACE = os.environ.get("APP_NAME", "service_notification")
CONFIG_CENTER_ENABLED = os.environ.get("CONFIG_CENTER_ENABLED", "false")

def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    if CONFIG_CENTER_ENABLED == "false":
        return {}
    else:
        return vault_factory()

def vault_factory() -> dict:
    vc = VaultClient(os.environ.get('VAULT_URL'), os.environ.get('VAULT_CRT'), os.environ.get('VAULT_TOKEN'))
    return vc.get_from_vault(SRV_NAMESPACE)


class Settings(BaseSettings):
    port: int = 5065
    host: str = "0.0.0.0"
    namespace: str = ""
    env: str = "test"
    OPEN_TELEMETRY_ENABLED: str
    NFS_ROOT_PATH = "./"
    VRE_ROOT_PATH = "/vre-data"
    ROOT_PATH = {
        "vre": "/vre-data"
    }.get(SRV_NAMESPACE, "/data/vre-storage")
    API_MODULES: List = ["service_email"]
    postfix: str = ""
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_port: str = ""
    POSTFIX_URL: str
    POSTFIX_PORT: str
    ALLOWED_EXTENSIONS: Set = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    IMAGE_EXTENSIONS: Set = set(['png', 'jpg', 'jpeg', 'gif'])
    RDS_HOST: str = ''
    RDS_PORT: str = ''
    RDS_USER: str = ''
    RDS_PWD: str = ''
    NOTIFICATIONS_DBNAME: str = 'notifications'
    NOTIFICATIONS_SCHEMA: str = 'notifications'
    ANNOUNCEMENTS_SCHEMA: str = 'announcements'
    version = "1.1.0"
    api_modules = API_MODULES
    SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USER}:{RDS_PWD}@{RDS_HOST}/{NOTIFICATIONS_DBNAME}"
    
    def update_db_uri(self):
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.RDS_USER}:{self.RDS_PWD}@{self.RDS_HOST}/{self.NOTIFICATIONS_DBNAME}"


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                load_vault_settings,
                env_settings,
                init_settings,
                file_secret_settings,
            )

@lru_cache(1)
def get_settings():
    settings = Settings()
    settings.update_db_uri()
    return settings

ConfigClass = get_settings()
