from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.appointment.entity.appointment_item_entity import AppointmentItemEntity


class AppointmentItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(AppointmentItemEntity,
                         filter_fields=[AppointmentItemEntity.appointment_id, AppointmentItemEntity.operator_id],
                         search_fields=[],
                         date_filters={
                             "from_datetime": (DateFilterEnum.FROM, AppointmentItemEntity.from_datetime),
                             "from_datetime_to": (DateFilterEnum.TO, AppointmentItemEntity.from_datetime),
                             "to_datetime_from": (DateFilterEnum.FROM, AppointmentItemEntity.to_datetime),
                             "to_datetime": (DateFilterEnum.TO, AppointmentItemEntity.to_datetime),
                         }
                         )
