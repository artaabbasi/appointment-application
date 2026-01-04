from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from common.api_manager.schema.api_schema import ApiSchema
from common.config.http_method_enum import HTTPMethodEnum


class ApiTagSchema(BaseModel):
    id: str
    name: str
    apis: Optional[List[ApiSchema]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

