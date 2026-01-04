from common.api_manager.schema.api_schema import ApiSchema
from common.lib.base_entity import BaseEntity
from sqlalchemy import Column, String, ARRAY


class ApiEntity(BaseEntity):
    __tablename__ = 'apis'

    name = Column(String(128), nullable=False)
    url = Column(String(128), nullable=False)
    methods = Column(ARRAY(String(64)), nullable=False)
    tags = Column(ARRAY(String(64)), nullable=False)

    def convert_to_schema(self) -> ApiSchema:
        return ApiSchema(
            id=self.id,
            name=self.name,
            url=self.url,
            methods=self.methods,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )