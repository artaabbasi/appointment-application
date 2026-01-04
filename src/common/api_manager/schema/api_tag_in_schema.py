from typing import List, Optional

from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum


class ApiTagInSchema(BaseModel):
    name: str
    apis: List[str] = []