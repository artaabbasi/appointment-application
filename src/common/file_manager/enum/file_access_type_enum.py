from enum import Enum


class FileAccessTypeEnum(str, Enum):
    PRIVATE = 'PRIVATE'
    LOCAL = 'LOCAL'
    PUBLIC = 'PUBLIC'
