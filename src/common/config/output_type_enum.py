from enum import Enum


class OutputTypeEnum(str, Enum):
    JSON = 'JSON'
    XLSX = 'XLSX'
    TEXT = 'TEXT'
