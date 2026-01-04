from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        Boolean,
                        DateTime,
                        Index,
                        and_, Integer
                        )

from common.lib.base_entity import BaseEntity
from common.settings import get_settings

settings = get_settings()


class UserEntity(BaseEntity):
    __tablename__ = 'users'

    username = Column(String(64), nullable=True)
    password = Column(String(1028), nullable=True)
    profile_id = Column(String(64), nullable=False)
    avatar = Column(String(64), nullable=True)
    verification_code = Column(String(6))
    verification_code_expires_at = Column(DateTime(timezone=True))
    is_verified = Column(Boolean, default=False)
    must_change_password = Column(Boolean, default=True)
    has_completed_profile = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True))
    group = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, serial={self.profile_id})>"


Index('profile_and_group_conditional_partial_unique_index',
      UserEntity.profile_id, UserEntity.group,
      unique=True,
      postgresql_where=and_(UserEntity.deleted_at.is_(None)))

Index('username_unique_index',
      UserEntity.username,
      unique=True,
      postgresql_where=and_(UserEntity.deleted_at.is_(None), UserEntity.username.is_not(None)))
