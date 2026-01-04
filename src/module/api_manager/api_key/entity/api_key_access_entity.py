from common.lib.base_entity import BaseEntity
from sqlalchemy import Column, String, ARRAY


class ApiKeyAccessEntity(BaseEntity):
    __tablename__ = 'api_key_access'

    api_key_id = Column(String(64), nullable=False)
    api_tag_id = Column(String(64), nullable=True)
    api_id = Column(String(64), nullable=True)
    methods = Column(ARRAY(String(64)), nullable=True)
