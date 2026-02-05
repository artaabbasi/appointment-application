
from common.appointment.schema.service_category_in_schema import ServiceCategoryInSchema
from common.appointment.schema.service_category_schema import ServiceCategorySchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.service_category_entity import ServiceCategoryEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.service_category_repository import ServiceCategoryRepository


class ServiceCategoryService(BaseCRUDService):
    def __init__(self):
        super().__init__(ServiceCategoryRepository, ServiceCategoryEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_service_category_by_id(self, service_category_id: str) -> ServiceCategorySchema:
        service_category = await self.repository.fetch_by_id(service_category_id)
        return service_category.convert_to_schema()

    async def get_service_category_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[ServiceCategorySchema]:
        service_categories = await self._list(page, size, filters, search)
        return [service_category.convert_to_schema() for service_category in service_categories]

    async def update_service_category(self, entity_id: str, schema: ServiceCategoryInSchema) -> ServiceCategorySchema:
        service_category = await self._update_by_id(schema, entity_id, is_partial=True)
        return service_category.convert_to_schema()

    async def delete_service_category(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_service_category(self, data_in: ServiceCategoryInSchema) -> ServiceCategorySchema:
        service_category = await self.repository.create(
            ServiceCategoryEntity(
                category_id=data_in.category_id,
                service_id=data_in.service_id,
            )
        )
        return service_category.convert_to_schema()
