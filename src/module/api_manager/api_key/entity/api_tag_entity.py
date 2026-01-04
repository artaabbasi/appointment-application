from common.api_manager.schema.api_tag_schema import ApiTagSchema
from common.lib.base_entity import BaseEntity
from sqlalchemy import Column, String, ARRAY


class ApiTagEntity(BaseEntity):
    __tablename__ = 'api_tags'

    name = Column(String(128), nullable=False)

    def convert_to_schema(self) -> ApiTagSchema:
        return ApiTagSchema(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )