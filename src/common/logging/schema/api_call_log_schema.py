from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum
from common.logging.enum.api_call_log_type_enum import ApiCalLogTypeEnum


class ApiCallLogSchema(BaseModel):
    id: str

    type: Optional[ApiCalLogTypeEnum] = None
    description: Optional[str] = None

    method: Optional[HTTPMethodEnum] = None
    url: Optional[str] = None
    headers: Optional[dict] = None
    payload: Union[dict, list, None] = None

    status_code: Optional[int] = None
    response_body: Union[dict, list, None] = None
    response_headers: Optional[dict] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
