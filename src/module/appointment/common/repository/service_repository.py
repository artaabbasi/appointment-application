from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.common.entity.service_entity import ServiceEntity


class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(ServiceEntity,
                         filter_fields=[ServiceEntity.main_service_id, ServiceEntity.is_active],
                         search_fields=[ServiceEntity.name])
