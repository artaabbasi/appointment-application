from typing import Optional, List

from sqlalchemy import select, and_, desc
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_system.entity.form_instance_entity import FormInstanceEntity


class FormInstanceRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormInstanceEntity,
                         filter_fields=[FormInstanceEntity.form_id,
                                        FormInstanceEntity.usage_type],
                         search_fields=[FormInstanceEntity.name],
                         order_by=[desc(FormInstanceEntity.created_at)])
