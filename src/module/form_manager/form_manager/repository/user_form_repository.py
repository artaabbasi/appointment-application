from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_manager.entity.user_form_entity import UserFormEntity


class UserFormRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserFormEntity)

    async def fetch_by_user_id_and_form_id(
            self,
            user_id: str,
            form_id: str,
    ) -> UserFormEntity:
        q = select(UserFormEntity)
        q = q.filter(and_(UserFormEntity.user_id == user_id,
                          UserFormEntity.form_id == form_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND)
        return entity
