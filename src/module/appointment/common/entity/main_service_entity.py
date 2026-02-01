from sqlalchemy import (Column,
                        String,
                        )

from common.lib.base_entity import BaseEntity


class MainServiceEntity(BaseEntity):
    __tablename__ = 'main_services'

    name = Column(String(1028), nullable=False)