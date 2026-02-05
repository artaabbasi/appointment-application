from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.appointment.entity.appointment_entity import AppointmentEntity


class AppointmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(AppointmentEntity,
                         filter_fields=[AppointmentEntity.user_id],
                         search_fields=[],
                         date_filters={
                             "created_from": (DateFilterEnum.FROM, AppointmentEntity.created_at),
                             "created_to": (DateFilterEnum.TO, AppointmentEntity.created_at),
                         })
