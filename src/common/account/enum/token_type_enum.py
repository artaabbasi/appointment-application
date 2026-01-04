from enum import Enum


class TokenTypeEnum(str, Enum):
    refresh = 'refresh'
    access = 'access'
    api_key = 'api_key'
