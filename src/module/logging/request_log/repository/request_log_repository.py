from typing import List, Optional

from sqlalchemy import select, and_, delete, desc
from sqlalchemy.exc import NoResultFound, IntegrityError

from common.exceptions import NotFoundException, InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.logging.request_log.entity.request_log_entity import RequestLogEntity


class RequestLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(RequestLogEntity,
                         filter_fields=[RequestLogEntity.url,
                                        RequestLogEntity.method,
                                        RequestLogEntity.response_status_code,
                                        RequestLogEntity.client,
                                        RequestLogEntity.type],
                         search_fields=[RequestLogEntity.url],
                         order_by=[desc(RequestLogEntity.created_at)])
