from typing import List, Optional

from sqlalchemy import select, and_, delete, desc
from sqlalchemy.exc import NoResultFound, IntegrityError

from common.exceptions import NotFoundException, InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.logging.api_call_log.entity.api_call_log_entity import ApiCallLogEntity


class ApiCallLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiCallLogEntity,
                         filter_fields=[ApiCallLogEntity.type,
                                        ApiCallLogEntity.method,
                                        ApiCallLogEntity.status_code,
                                        ApiCallLogEntity.url,
                                        ApiCallLogEntity.description],
                         search_fields=[ApiCallLogEntity.url,
                                        ApiCallLogEntity.description],
                         date_filters={
                             "created_from": (DateFilterEnum.FROM, ApiCallLogEntity.created_at),
                             "created_to": (DateFilterEnum.TO, ApiCallLogEntity.created_at),
                         },
                         order_by=[desc(ApiCallLogEntity.created_at)])


