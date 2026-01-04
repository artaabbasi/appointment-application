from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum


class ApiSchema(BaseModel):
    id: str
    name: str
    url: str
    methods: List[HTTPMethodEnum]
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

