from common.appointment.schema.main_service_in_schema import MainServiceInSchema
from common.appointment.schema.main_service_schema import MainServiceSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.main_service_entity import MainServiceEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.main_service_repository import MainServiceRepository


class MainServiceService(BaseCRUDService):
    def __init__(self):
        super().__init__(MainServiceRepository, MainServiceEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_main_service_by_id(self, main_service_id: str) -> MainServiceSchema:
        main_service = await self.repository.fetch_by_id(main_service_id)
        return main_service.convert_to_schema()

    async def get_main_service_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[MainServiceSchema]:
        specialities = await self._list(page, size, filters, search)
        return [main_service.convert_to_schema() for main_service in specialities]

    async def update_main_service(self, entity_id: str, schema: MainServiceInSchema) -> MainServiceSchema:
        main_service = await self._update_by_id(schema, entity_id, is_partial=True)
        return main_service.convert_to_schema()

    async def delete_main_service(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_main_service(self, data_in: MainServiceInSchema) -> MainServiceSchema:
        main_service = await self.repository.create(
            MainServiceEntity(
                name=data_in.name
            )
        )
        return main_service.convert_to_schema()
