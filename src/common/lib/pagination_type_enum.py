from enum import Enum


class PaginationTypeEnum(str, Enum):
    SKIP_LIMIT = 'SKIP_LIMIT',
    PAGE_SIZE = 'PAGE_SIZE'
