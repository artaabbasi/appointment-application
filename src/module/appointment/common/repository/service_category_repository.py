from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.common.entity.service_category_entity import ServiceCategoryEntity


class ServiceCategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(ServiceCategoryEntity,
                         filter_fields=[ServiceCategoryEntity.service_id, ServiceCategoryEntity.category_id],
                         search_fields=[]
                         )
