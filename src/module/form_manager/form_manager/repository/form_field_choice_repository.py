from typing import List

from sqlalchemy import delete, and_, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from common.exceptions import InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_manager.entity.form_field_choice_entity import FormFieldChoiceEntity


class FormFieldChoiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormFieldChoiceEntity)

    async def delete_by_field_id_and_not_ids(self, field_id: str, ids: list[str]):
        q = delete(FormFieldChoiceEntity)
        q = q.filter(and_(FormFieldChoiceEntity.field_id == field_id,
                          FormFieldChoiceEntity.id.not_in(ids)))
        try:
            async with get_session() as session:
                await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def fetch_by_field_id(
            self,
            field_id: str,
    ) -> List[FormFieldChoiceEntity]:
        q = select(FormFieldChoiceEntity)
        q = q.filter(and_(FormFieldChoiceEntity.field_id == field_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound as error:
            entities = []
        return entities
