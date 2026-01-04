from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        Boolean,
                        Integer,
                        Index,
                        and_
                        )

from common.lib.base_entity import BaseEntity
from common.settings import get_settings

settings = get_settings()


class ProfileEntity(BaseEntity):
    __tablename__ = 'profiles'

    id = Column(String(64), primary_key=True)
    email = Column(String(256), nullable=True)
    first_name = Column(String(256), nullable=True)
    en_first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    en_last_name = Column(String(256), nullable=True)
    father_name = Column(String(256), nullable=True)
    phone_number = Column(String(16), nullable=False)
    birth_date = Column(String(32), nullable=True)
    national_code = Column(String(32), nullable=True)


    def __repr__(self):
        return f"<Profile(id={self.id}, serial={self.phone_number})>"


Index('phone_number_partial_unique_index',
      ProfileEntity.phone_number,
      unique=True,
      postgresql_where=and_(ProfileEntity.deleted_at.is_(None)))
