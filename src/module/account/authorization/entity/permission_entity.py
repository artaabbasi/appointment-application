from sqlalchemy import Column, String

from common.account.schema.permission_schema import PermissionSchema
from common.lib.base_entity import BaseEntity


class PermissionEntity(BaseEntity):
    __tablename__ = "permissions"
    title = Column(String(64), nullable=True)
    module = Column(String(64), nullable=False)
    sub_module = Column(String(64), nullable=False)
    action = Column(String(64), nullable=False)

    def convert_to_schema(self):
        return PermissionSchema(
            id=self.id,
            title=self.title,
            module=self.module,
            sub_module=self.sub_module,
            action=self.action,
        )