from typing import Optional, List

from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_manager.entity.form_entity import FormEntity


class FormRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormEntity)

    async def fetch_by_service_id_and_service_type(
            self,
            service_id: str,
            service_type: str,
    ) -> FormEntity:
        q = select(FormEntity)
        q = q.filter(and_(FormEntity.service_type == service_type,
                          FormEntity.service_id == service_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND)
        return entity
