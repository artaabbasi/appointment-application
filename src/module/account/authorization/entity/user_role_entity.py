from sqlalchemy import Column, String, Index, and_

from common.lib.base_entity import BaseEntity


class UserRoleEntity(BaseEntity):
    __tablename__ = "user_roles"
    role_id = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)


Index('user_role_user_id_index',
      UserRoleEntity.user_id,
      postgresql_where=and_(UserRoleEntity.deleted_at.is_(None)))
