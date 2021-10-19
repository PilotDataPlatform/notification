import os
import requests
from requests.models import HTTPError
from pydantic import BaseSettings, Extra
from typing import Dict, Set, List, Any
from functools import lru_cache

SRV_NAMESPACE = os.environ.get("APP_NAME", "service_notification")
CONFIG_CENTER_ENABLED = os.environ.get("CONFIG_CENTER_ENABLED", "false")
CONFIG_CENTER_BASE_URL = os.environ.get("CONFIG_CENTER_BASE_URL", "NOT_SET")

def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    if CONFIG_CENTER_ENABLED == "false":
        return {}
    else:
        return vault_factory(CONFIG_CENTER_BASE_URL)

def vault_factory(config_center) -> dict:
    url = config_center + \
        "/v1/utility/config/{}".format(SRV_NAMESPACE)
    config_center_respon = requests.get(url)
    if config_center_respon.status_code != 200:
        raise HTTPError(config_center_respon.text)
    return config_center_respon.json()['result']


class Settings(BaseSettings):
    port: int = 5065
    host: str = "0.0.0.0"

    NFS_ROOT_PATH = "./"
    VRE_ROOT_PATH = "/vre-data"
    ROOT_PATH = {
        "vre": "/vre-data"
    }.get(SRV_NAMESPACE, "/data/vre-storage")

    # the packaged modules
    API_MODULES: List = ["service_email"]
    POSTFIX: str = ""
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_PORT: str = ""

    POSTFIX_URL: str
    POSTFIX_PORT: str

    ALLOWED_EXTENSIONS: Set = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    IMAGE_EXTENSIONS: Set = set(['png', 'jpg', 'jpeg', 'gif'])

    RDS_HOST: str
    RDS_PORT: str
    RDS_DBNAME: str = ""
    RDS_USER: str
    RDS_PWD: str
    RDS_SCHEMA_DEFAULT:str 


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
    settings =  Settings()
    return settings

class ConfigClass(object):
    settings = get_settings()

    version = "1.1.0"

    # disk mounts
    NFS_ROOT_PATH = settings.NFS_ROOT_PATH
    VRE_ROOT_PATH = settings.VRE_ROOT_PATH
    ROOT_PATH = settings.ROOT_PATH

    # the packaged modules
    api_modules = settings.API_MODULES
    postfix = settings.POSTFIX
    smtp_user = settings.SMTP_USER
    smtp_pass = settings.SMTP_PASS
    smtp_port = settings.SMTP_PORT

    POSTFIX_URL = settings.POSTFIX_URL
    POSTFIX_PORT = settings.POSTFIX_PORT

    ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


    RDS_HOST = settings.RDS_HOST
    RDS_PORT = settings.RDS_PORT
    RDS_DBNAME = settings.RDS_DBNAME
    RDS_USER = settings.RDS_USER
    RDS_PWD = settings.RDS_PWD
    RDS_SCHEMA_DEFAULT = settings.RDS_SCHEMA_DEFAULT
    SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USER}:{RDS_PWD}@{RDS_HOST}/{RDS_DBNAME}"


