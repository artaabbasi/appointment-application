from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.appointment.entity.cart_entity import CartEntity
from util.timestamp import DatetimeUtil


class CartRepository(BaseRepository):
    def __init__(self):
        super().__init__(CartEntity,
                         filter_fields=[CartEntity.user_id],
                         search_fields=[],
                         date_filters={
                             "created_from": (DateFilterEnum.FROM, CartEntity.created_at),
                             "created_to": (DateFilterEnum.TO, CartEntity.created_at),
                             "valid_to": (DateFilterEnum.TO, CartEntity.valid_to),
                         })

    async def fetch_active_by_user_id(
            self,
            user_id: str,
    ) -> CartEntity:
        q = select(CartEntity)
        q = q.filter(and_(CartEntity.user_id == user_id, CartEntity.valid_to > DatetimeUtil.utc_now_datetime()))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND, user_id)
        return entity
