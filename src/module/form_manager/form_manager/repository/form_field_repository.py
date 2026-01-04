from typing import List

from sqlalchemy import delete, and_, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from common.exceptions import InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_manager.entity.form_field_entity import FormFieldEntity


class FormFieldRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormFieldEntity)

    async def delete_by_form_id_and_not_ids(self, form_id: str, ids: list[str]):
        q = delete(FormFieldEntity)
        q = q.filter(and_(FormFieldEntity.form_id == form_id,
                          FormFieldEntity.id.not_in(ids)))
        try:
            async with get_session() as session:
                await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def fetch_by_form_id(
            self,
            form_id: str,
    ) -> List[FormFieldEntity]:
        q = select(FormFieldEntity)
        q = q.filter(and_(FormFieldEntity.form_id == form_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound as error:
            entities = []
        return entities

