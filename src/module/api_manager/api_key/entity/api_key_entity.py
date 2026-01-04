from common.api_manager.schema.api_key_schema import ApiKeySchema
from common.lib.base_entity import BaseEntity
from sqlalchemy import Column, String


class ApiKeyEntity(BaseEntity):
    __tablename__ = 'api_key'

    user_id = Column(String(64), nullable=False)
    name = Column(String(128), nullable=False)


    def convert_to_schema(self):
        return ApiKeySchema(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            accesses=[],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )