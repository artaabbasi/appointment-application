from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.common.entity.operator_entity import OperatorEntity


class OperatorRepository(BaseRepository):
    def __init__(self):
        super().__init__(OperatorEntity,
                         filter_fields=[],
                         search_fields=[OperatorEntity.name])
