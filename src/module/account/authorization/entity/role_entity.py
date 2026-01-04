from sqlalchemy import Column, String, Boolean

from common.account.schema.role_schema import RoleSchema
from common.lib.base_entity import BaseEntity


class RoleEntity(BaseEntity):
    __tablename__ = "roles"
    name = Column(String(128), nullable=False)
    title = Column(String(128), nullable=True)
    show_in_site = Column(Boolean, default=lambda: True, server_default="true", nullable=True)

    def convert_to_schema(self):
        return RoleSchema(
            id=self.id,
            name=self.name,
            title=self.title,
            show_in_site=self.show_in_site,
        )
