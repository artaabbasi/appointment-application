from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        Boolean,
                        Index,
                        and_
                        )

from common.lib.base_entity import BaseEntity


class StaffEntity(BaseEntity):
    __tablename__ = 'staffs'

    user_id = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<staff(id={self.id}, user={self.user_id})>"


Index('user_id_partial_unique_index',
      StaffEntity.user_id,
      unique=True,
      postgresql_where=and_(StaffEntity.deleted_at.is_(None)))
