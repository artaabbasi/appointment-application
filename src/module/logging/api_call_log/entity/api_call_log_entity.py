from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        JSON,
                        Integer,
                        Text,
                        )

from common.lib.base_entity import BaseEntity
from common.logging.schema.api_call_log_schema import ApiCallLogSchema

class ApiCallLogEntity(BaseEntity):
    __tablename__ = 'api_call_log'

    type = Column(String(64), nullable=True)
    description = Column(String(64), nullable=True)

    method = Column(String(64), nullable=True)
    url = Column(Text, nullable=True)
    headers = Column(JSON, nullable=True)
    payload = Column(JSON, nullable=True)

    status_code = Column(Integer, nullable=True)
    response_body = Column(JSON, nullable=True)
    response_headers = Column(JSON, nullable=True)

    def convert_to_schema(self) -> ApiCallLogSchema:
        return ApiCallLogSchema(
            id=self.id,
            type=self.type,
            description=self.description,
            method=self.method,
            url=self.url,
            headers=self.headers,
            payload=self.payload,
            status_code=self.status_code,
            response_body=self.response_body,
            response_headers=self.response_headers,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
