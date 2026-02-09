import os.path
import sys
from os import path
from enum import Enum
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentEnum(str, Enum):
    TEST = 'TEST'
    KB = 'KB'
    DEVELOPMENT = 'DEVELOPMENT'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'
    BG_TASK = 'BG_TASK'


class Settings(BaseSettings):
    """
    This class will read its attributes from multiple sources. For more information check
    pydantic's documentation.
    https://pydantic-docs.helpmanual.io/usage/settings

    Source priority.
    https://pydantic-docs.helpmanual.io/usage/settings/#field-value-priority
    """
    model_config = SettingsConfigDict(env_file=path.join(path.dirname(path.abspath(__file__)), '..', '..', '.env'))
    PROJECT_NAME: str = "backend"

    ENV: EnvironmentEnum = Field(..., alias='ENV')

    CORS_ALLOW_ORIGINS: List[str] = Field(['*'], alias='CORS_ALLOW_ORIGINS')

    DATABASE_HOST: str = Field(..., alias='DATABASE_HOST')
    DATABASE_PORT: int = Field(5432, alias='DATABASE_PORT')
    DATABASE_NAME: str = Field(..., alias='DATABASE_NAME')
    DATABASE_USER: str = Field(..., alias='DATABASE_USER')
    DATABASE_PASSWORD: str = Field(..., alias='DATABASE_PASSWORD')

    TEST_DATABASE_HOST: str = Field(None, alias='TEST_DATABASE_HOST')
    TEST_DATABASE_PORT: int = Field(5432, alias='TEST_DATABASE_PORT')
    TEST_DATABASE_NAME: str = Field(None, alias='TEST_DATABASE_NAME')
    TEST_DATABASE_USER: str = Field(None, alias='TEST_DATABASE_USER')
    TEST_DATABASE_PASSWORD: str = Field(None, alias='TEST_DATABASE_PASSWORD')

    RSA_PRIVATE_KEY: str = Field(..., alias='RSA_PRIVATE_KEY')
    RSA_PUBLIC_KEY: str = Field(..., alias='RSA_PUBLIC_KEY')


    MEDIA_DIRECTORY: str = Field('media/', alias='MEDIA_DIRECTORY')
    BASE_DICTIONARY_DIRECTORY: str = Field('common/config/dictionary/', alias='BASE_DICTIONARY_DIRECTORY')
    MIME_TYPES_FILE: str = Field('module/file_manager/bucket/config/mime_types.yaml', alias='MIME_TYPES_FILE')

    DEFAULT_USERNAME: str = Field(None, alias='DEFAULT_USERNAME')
    DEFAULT_PASSWORD: str = Field(None, alias='DEFAULT_PASSWORD')
    DEFAULT_PHONE: str = Field(None, alias='DEFAULT_PHONE')

    REDIS_HOST: str = Field(..., alias='REDIS_HOST')
    REDIS_PORT: int = Field(6379, alias='REDIS_PORT')
    REDIS_PASSWORD: str = Field(..., alias='REDIS_PASSWORD')

    ACCESS_TOKEN_EXPIRATION_TIME_DELTA_MINUTES: int = Field(..., alias='ACCESS_TOKEN_EXPIRATION_TIME_DELTA_MINUTES')
    REFRESH_TOKEN_EXPIRATION_TIME_DELTA_MINUTES: int = Field(..., alias='REFRESH_TOKEN_EXPIRATION_TIME_DELTA_MINUTES')
    API_TOKEN_EXPIRATION_TIME_DELTA_MINUTES: int = Field(..., alias='API_TOKEN_EXPIRATION_TIME_DELTA_MINUTES')

    CART_VALID_SECS: int = Field(60, alias='CART_VALID_SECS')
    IP_PANEL_GATEWAY: str = Field(..., alias='IP_PANEL_GATEWAY')
    IP_PANEL_SMS_SENDER: str = Field(..., alias='IP_PANEL_SMS_SENDER')
    IP_PANEL_API_KEY: str = Field(..., alias='IP_PANEL_API_KEY')

def get_settings():
    settings = Settings()
    return settings
