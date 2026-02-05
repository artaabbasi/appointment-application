from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.common.entity.operator_time_entity import OperatorTimeEntity


class OperatorTimeRepository(BaseRepository):
    def __init__(self):
        super().__init__(OperatorTimeEntity,
                         filter_fields=[OperatorTimeEntity.operator_id],
                         search_fields=[],
                         date_filters={
                             "from_datetime": (DateFilterEnum.FROM, OperatorTimeEntity.from_datetime),
                             "to_datetime": (DateFilterEnum.TO, OperatorTimeEntity.to_datetime),
                         }
                         )
