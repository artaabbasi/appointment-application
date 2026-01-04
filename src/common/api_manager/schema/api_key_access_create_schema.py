from typing import List, Optional
from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum


class CreateApiKeyApiAccessSchema(BaseModel):
    api_id: Optional[str] = None
    methods: Optional[List[HTTPMethodEnum]] = []

class CreateApiKeyApiTagAccessSchema(BaseModel):
    api_tag_id: Optional[str] = None


class ListCreateApiKeyAccessSchema(BaseModel):
    user_id: str
    tags: List[CreateApiKeyApiTagAccessSchema]
    apis: List[CreateApiKeyApiAccessSchema]
