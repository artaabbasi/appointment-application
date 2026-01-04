from typing import Optional, List

from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_manager.entity.user_form_change_log_entity import UserFormChangeLogEntity


class UserFormChangeLogRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserFormChangeLogEntity,
                         filter_fields=[UserFormChangeLogEntity.user_form_id,
                                        UserFormChangeLogEntity.user_id])
