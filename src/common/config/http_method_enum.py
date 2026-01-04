from enum import Enum
from typing import Optional


class HTTPMethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"

    @staticmethod
    def get_enum_from_str(method: str) -> Optional['HTTPMethodEnum']:
        for meth in HTTPMethodEnum:
            if meth.value.lower() == method.lower():
                return meth
        return None
