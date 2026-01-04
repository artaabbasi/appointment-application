from sqlalchemy import Column, String, Boolean

from common.lib.base_entity import BaseEntity


class UserPermissionEntity(BaseEntity):
    __tablename__ = "user_permissions"
    user_id = Column(String(64), nullable=False)
    permission_id = Column(String(64), nullable=False)
    had_access_to_all = Column(Boolean, nullable=False, default=False)
