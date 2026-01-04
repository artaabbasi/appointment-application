from typing import List, Optional

from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum


class ApiInSchema(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    methods: Optional[List[HTTPMethodEnum]] = None
    tags: Optional[List[str]] = None
