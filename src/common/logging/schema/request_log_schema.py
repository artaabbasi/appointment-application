from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum
from common.logging.enum.request_log_type_enum import RequestLogTypeEnum


class RequestLogSchema(BaseModel):
    id: Optional[str] = None
    type: Optional[RequestLogTypeEnum] = None
    url: Optional[str] = None
    method: Optional[HTTPMethodEnum] = None
    client: Optional[str] = None
    process_time: Optional[float] = None
    request_headers: Optional[str] = None
    request_payload: Optional[str] = None
    response_status_code: Optional[int] = None
    response_body: Optional[str] = None
    response_headers: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None