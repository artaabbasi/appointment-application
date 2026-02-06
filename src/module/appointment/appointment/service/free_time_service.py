from datetime import datetime
from typing import List

from common.appointment.schema.reserved_time_schema import ReservedTimeSchema
from common.lib.base_service import BaseService
from module.appointment.appointment.entity.appointment_item_entity import AppointmentItemEntity
from module.appointment.appointment.entity.cart_entity import CartEntity
from module.appointment.appointment.entity.cart_item_entity import CartItemEntity
from module.appointment.appointment.service.appointment_item_service import AppointmentItemService
from module.appointment.appointment.service.cart_item_service import CartItemService
from module.appointment.appointment.service.cart_service import CartService
from util.timestamp import DatetimeUtil


class FreeTimeService(BaseService):
    def __init__(self):
        self.cart_service = CartService()
        self.cart_item_service = CartItemService()
        self.appointment_item_service = AppointmentItemService()

    async def get_operator_reserved_times(self, operator_id: str, from_datetime: datetime, to_datetime: datetime) -> List[ReservedTimeSchema]:
        active_carts = await self.cart_service.get_cart_list(page=1, size=-1,
                                                             filters={"valid_to": DatetimeUtil.utc_now_datetime()})
        reserved_times = []
        for cart in active_carts:
            active_cart_items = await self.cart_item_service.get_cart_item_list(page=1, size=-1,
                                                                                filters={CartItemEntity.cart_id: cart.id,
                                                                                         CartItemEntity.operator_id: operator_id,
                                                                                         "to_datetime_from": from_datetime,
                                                                                         "from_datetime_to": to_datetime
                                                                                         })
            for active_cart_item in active_cart_items:
                reserved_times.append(
                    ReservedTimeSchema(
                        from_datetime=active_cart_item.from_datetime,
                        to_datetime=active_cart_item.to_datetime,
                    )
                )
        appointment_items = await self.appointment_item_service.get_appointment_item_list(page=1, size=-1,
                                                                                          filters={AppointmentItemEntity.operator_id: operator_id,
                                                                                                   "to_datetime_from": from_datetime,
                                                                                                   "from_datetime_to": to_datetime})
        for appointment_item in appointment_items:
            reserved_times.append(
                ReservedTimeSchema(
                    from_datetime=appointment_item.from_datetime,
                    to_datetime=appointment_item.to_datetime,
                )
            )
        sorted_reserved_times = sorted(reserved_times, key=lambda x: x.from_datetime, reverse=False)
        return sorted_reserved_times

    async def check_operator_can_reserve(self, operator_id: str, from_datetime: datetime, to_datetime: datetime) -> bool:
        if from_datetime < DatetimeUtil.utc_now_datetime():
            return False
        reserved_times = await self.get_operator_reserved_times(operator_id, from_datetime, to_datetime)
        return not bool(reserved_times)


