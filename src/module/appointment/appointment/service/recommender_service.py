import random
from datetime import timedelta
from typing import List

from common.appointment.schema.recommended_item_schema import RecommendItemSchema
from common.appointment.schema.reserved_time_schema import ReservedTimeSchema
from common.lib.base_service import BaseService
from module.appointment.appointment.entity.cart_item_entity import CartItemEntity
from module.appointment.appointment.service.cart_item_service import CartItemService
from module.appointment.appointment.service.cart_service import CartService
from module.appointment.appointment.service.free_time_service import FreeTimeService
from module.appointment.common.entity.operator_service_entity import OperatorServiceEntity
from module.appointment.common.entity.service_category_entity import ServiceCategoryEntity
from module.appointment.common.service.operator_service_service import OperatorServiceService
from module.appointment.common.service.service_category_service import ServiceCategoryService
from module.appointment.common.service.service_service import ServiceService


class RecommenderService(BaseService):
    def __init__(self):
        self.cart_service = CartService()
        self.cart_item_service = CartItemService()
        self.service_category_service = ServiceCategoryService()
        self.service_service = ServiceService()
        self.operator_service_service = OperatorServiceService()
        self.free_time_service = FreeTimeService()

    async def _get_cart_times(self, cart_id: str) -> List[ReservedTimeSchema]:
        cart_times = []
        cart_items = await self.cart_item_service.get_cart_item_list(page=1, size=-1, filters={CartItemEntity.cart_id: cart_id})
        sorted_cart_items = sorted(cart_items, key=lambda _cart_item: cart_item.from_datetime, reverse=False)
        for cart_item in sorted_cart_items:
            cart_times.append(
                ReservedTimeSchema(
                    from_datetime=cart_item.from_datetime,
                    to_datetime=cart_item.to_datetime,
                )
            )
        return cart_times

    async def _get_recommended_service_times(self, cart_id: str, service_ids: List[str]) -> List[RecommendItemSchema]:
        cart_times = await self._get_cart_times(cart_id)
        if not cart_times:
            return []
        recommended_service_times = []
        for service_id in service_ids:
            service = await self.service_service.get_service_by_id(service_id)
            service_operators = await self.operator_service_service.get_operator_service_list(page=1, size=-1,
                                                                                              filters={OperatorServiceEntity.service_id: service.id})
            first_time = cart_times[0]
            first_to_time = first_time.from_datetime
            first_from_time = first_to_time - timedelta(seconds=service.duration)
            last_time = cart_times[-1]
            last_from_time = last_time.to_datetime
            last_to_time = last_from_time + timedelta(seconds=service.duration)
            for service_operator in service_operators:
                if await self.free_time_service.check_operator_can_reserve(service_operator.operator_id, first_from_time, first_to_time):
                    recommended_service_times.append(
                        RecommendItemSchema(
                            service_id=service_id,
                            operator_id=service_operator.operator_id,
                            from_datetime=first_from_time,
                            to_datetime=first_to_time,
                        )
                    )
                if await self.free_time_service.check_operator_can_reserve(service_operator.operator_id, last_from_time, last_to_time):
                    recommended_service_times.append(
                        RecommendItemSchema(
                            service_id=service_id,
                            operator_id=service_operator.operator_id,
                            from_datetime=last_from_time,
                            to_datetime=last_to_time,
                        )
                    )
        return recommended_service_times


    async def get_recommended_services_for_cart_id(self, cart_id: str) -> List[RecommendItemSchema]:
        cart_items = await self.cart_item_service.get_cart_item_list(page=1, size=-1, filters={CartItemEntity.cart_id: cart_id})
        cart_service_ids = [cart_item.service_id for cart_item in cart_items]
        can_recommend_service_ids = []
        for selected_service_id in cart_service_ids:
            service_categories = await self.service_category_service.get_service_category_list \
                                         (page=1, size=-1, filters={ServiceCategoryEntity.service_id: selected_service_id})
            same_category_service_ids = []
            for service_category in service_categories:
                same_service_categories = await self.service_category_service.get_service_category_list \
                                         (page=1, size=-1, filters={ServiceCategoryEntity.category_id: service_category.category_id})
                same_category_service_ids.extend([same_service_category.service_id
                                                  for same_service_category in same_service_categories
                                                  if same_service_category.service_id != selected_service_id
                                                  and same_service_category.service_id not in cart_service_ids])
            if same_category_service_ids:
                can_recommend_service_ids.extend(same_category_service_ids)
            else:
                selected_service = await self.service_service.get_service_by_id(selected_service_id)
                other_services = await self.service_service.get_service_list(page=1, size=-1)
                for service in other_services:
                    if (service.id not in cart_service_ids
                            and service.id != selected_service_id
                            and service.main_service_id != selected_service.main_service_id):
                        can_recommend_service_ids.append(service.id)
        return await self._get_recommended_service_times(cart_id, can_recommend_service_ids)

