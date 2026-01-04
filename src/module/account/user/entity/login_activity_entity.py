from __future__ import annotations

from typing import Optional

from sqlalchemy import (Column,
                        String,
                        Text,
                        Index,
                        Integer,
                        and_
                        )

from common.account.schema.login_activity_schema import LoginActivitySchema
from common.lib.base_entity import BaseEntity


class LoginActivityEntity(BaseEntity):
    __tablename__ = 'login_activity'

    user_id = Column(String(64), nullable=False)
    refresh_token = Column(Text, nullable=False)
    expire_timestamp = Column(Integer, nullable=False)
    ip_address = Column(String(64), nullable=True)
    agent = Column(Text, nullable=True)

    def __repr__(self):
        return f"<login_activity(id={self.id}, user={self.user_id})>"

    def convert_to_schema(self, refresh_token: Optional[str] = None):
        return LoginActivitySchema(
            id=self.id,
            user_id=self.user_id,
            expire_timestamp=self.expire_timestamp,
            ip_address=self.ip_address,
            agent=self.agent,
            is_current=self.refresh_token == refresh_token,
            created_at=self.created_at,
        )


Index('login_refresh_token_index',
      LoginActivityEntity.refresh_token,
      postgresql_where=and_(LoginActivityEntity.deleted_at.is_(None)))

Index('login_user_id_and_timestamp_index',
      LoginActivityEntity.user_id, LoginActivityEntity.expire_timestamp,
      postgresql_where=and_(LoginActivityEntity.deleted_at.is_(None)))
