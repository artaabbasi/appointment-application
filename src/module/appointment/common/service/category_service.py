from common.appointment.schema.category_in_schema import CategoryInSchema
from common.appointment.schema.category_schema import CategorySchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.category_entity import CategoryEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.category_repository import CategoryRepository


class CategoryService(BaseCRUDService):
    def __init__(self):
        super().__init__(CategoryRepository, CategoryEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_category_by_id(self, category_id: str) -> CategorySchema:
        category = await self.repository.fetch_by_id(category_id)
        return category.convert_to_schema()

    async def get_category_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[CategorySchema]:
        specialities = await self._list(page, size, filters, search)
        return [category.convert_to_schema() for category in specialities]

    async def update_category(self, entity_id: str, schema: CategoryInSchema) -> CategorySchema:
        category = await self._update_by_id(schema, entity_id, is_partial=True)
        return category.convert_to_schema()

    async def delete_category(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_category(self, data_in: CategoryInSchema) -> CategorySchema:
        category = await self.repository.create(
            CategoryEntity(
                name=data_in.name
            )
        )
        return category.convert_to_schema()
