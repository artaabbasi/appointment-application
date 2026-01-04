from enum import Enum


class TimeTypeEnum(str, Enum):
    DAILY = 'DAILY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'
