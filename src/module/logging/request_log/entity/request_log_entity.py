from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        JSON, Float,
                        Integer,
                        Text, Time
                        )

from common.lib.base_entity import BaseEntity
from common.logging.schema.request_log_schema import RequestLogSchema

class RequestLogEntity(BaseEntity):
    __tablename__ = 'request_log'

    type = Column(String(64), nullable=True)

    url = Column(Text, nullable=True)
    process_time = Column(Float, nullable=True)

    method = Column(String(64), nullable=True)
    client = Column(Text, nullable=True)

    request_headers = Column(Text, nullable=True)
    request_payload = Column(Text, nullable=True)

    response_status_code = Column(Integer, nullable=True)
    response_body = Column(Text, nullable=True)
    response_headers = Column(Text, nullable=True)

    def convert_to_schema(self) -> RequestLogSchema:
        return RequestLogSchema(
            id=self.id,
            type=self.type,
            url=self.url,
            process_time=self.process_time,
            method=self.method,
            client=self.client,
            request_headers=self.request_headers,
            request_payload=self.request_payload,
            response_status_code=self.response_status_code,
            response_body=self.response_body,
            response_headers=self.response_headers,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
