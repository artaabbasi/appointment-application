from sqlalchemy import Column, String, Index, and_, Boolean

from common.lib.base_entity import BaseEntity


class RolePermissionEntity(BaseEntity):
    __tablename__ = "role_permissions"
    role_id = Column(String(64), nullable=False)
    permission_id = Column(String(64), nullable=False)
    had_access_to_all = Column(Boolean, nullable=True, default=False)


Index('role_permission_role_index',
      RolePermissionEntity.role_id,
      postgresql_where=and_(RolePermissionEntity.deleted_at.is_(None)))

Index('role_permission_permission_index',
      RolePermissionEntity.permission_id,
      postgresql_where=and_(RolePermissionEntity.deleted_at.is_(None)))

