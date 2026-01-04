from typing import List, Optional

from pydantic import BaseModel

from common.config.http_method_enum import HTTPMethodEnum


class ApiKeyAccessSchema(BaseModel):
    api_id: Optional[str] = None
    api_tag_id: Optional[str] = None
    api_name: Optional[str] = None
    api_url: Optional[str] = None
    api_tags: Optional[List[str]] = []
    api_methods: Optional[List[HTTPMethodEnum]] = []
    access_methods: Optional[List[HTTPMethodEnum]] = []
