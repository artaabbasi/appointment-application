from enum import Enum


class UserGroupEnum(str, Enum):
    admin = 'admin'
    customer = 'customer'
    api_key = 'api_key'

