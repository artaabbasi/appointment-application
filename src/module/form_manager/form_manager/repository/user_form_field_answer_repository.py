from typing import List

from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.form_manager.form_manager.entity.user_form_field_answer_entity import UserFormFieldAnswerEntity


class UserFormFieldAnswerRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserFormFieldAnswerEntity)

    async def fetch_by_user_form_id(
            self,
            user_form_id: str,
    ) -> List[UserFormFieldAnswerEntity]:
        q = select(UserFormFieldAnswerEntity)
        q = q.filter(and_(UserFormFieldAnswerEntity.user_form_id == user_form_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound as error:
            entities = []
        return entities

    async def fetch_by_user_form_id_and_form_field_id(
            self,
            user_form_id: str,
            form_field_id: str,
    ) -> UserFormFieldAnswerEntity:
        q = select(UserFormFieldAnswerEntity)
        q = q.filter(and_(UserFormFieldAnswerEntity.user_form_id == user_form_id,
                          UserFormFieldAnswerEntity.form_field_id == form_field_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().first()
        except NoResultFound as error:
            entity = None
        return entity
