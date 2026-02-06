from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.appointment.appointment.entity.cart_item_entity import CartItemEntity


class CartItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(CartItemEntity,
                         filter_fields=[CartItemEntity.cart_id, CartItemEntity.id, CartItemEntity.operator_id],
                         search_fields=[],
                         date_filters={
                             "from_datetime": (DateFilterEnum.FROM, CartItemEntity.from_datetime),
                             "from_datetime_to": (DateFilterEnum.TO, CartItemEntity.from_datetime),
                             "to_datetime_from": (DateFilterEnum.FROM, CartItemEntity.to_datetime),
                             "to_datetime": (DateFilterEnum.TO, CartItemEntity.to_datetime),
                         }
                         )
