from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.common.entity.operator_service_entity import OperatorServiceEntity


class OperatorServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(OperatorServiceEntity,
                         filter_fields=[OperatorServiceEntity.operator_id],
                         search_fields=[]
                         )
