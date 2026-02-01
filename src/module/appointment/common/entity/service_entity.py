from sqlalchemy import (Column,
                        String, Integer,
                        )

from common.lib.base_entity import BaseEntity


class ServiceEntity(BaseEntity):
    __tablename__ = 'services'

    main_service_id = Column(String(64), nullable=False)
    name = Column(String(1028), nullable=False)
    duration = Column(Integer, nullable=False)