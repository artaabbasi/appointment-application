from typing import List

from common.exceptions import NotFoundException
from common.form_manager.schema.form_instance_in_schema import FormInstanceInSchema
from common.form_manager.schema.form_instance_schema import FormInstanceSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.form_manager.form_system.entity.form_instance_entity import FormInstanceEntity
from module.form_manager.form_system.repository.form_instance_assignment_repository import \
    FormInstanceAssignmentRepository
from module.form_manager.form_system.repository.form_instance_repository import FormInstanceRepository
from util.timestamp import DatetimeUtil


class FormInstanceService(BaseCRUDService):
    def __init__(self):
        super().__init__(FormInstanceRepository, FormInstanceEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.form_instance_assignment_repository = FormInstanceAssignmentRepository()

    async def get_form_instance_list(self,
                                    page: int = 1,
                                    size: int = 10,
                                    filters: dict = None,
                                    search: str = "") \
            -> list[FormInstanceSchema]:
        form_instances = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return [form_instance.convert_to_schema() for form_instance in form_instances]

    async def get_by_id(self, form_instance_id: str) -> FormInstanceSchema:
        form_instance = await self.repository.fetch_by_id(form_instance_id)
        return form_instance.convert_to_schema()

    async def get_by_ids(self, form_instance_ids: List[str]) -> List[FormInstanceSchema]:
        form_instances = await self.repository.fetch_all_by_ids(form_instance_ids)
        return [form_instance.convert_to_schema() for form_instance in form_instances]

    async def update_form_instance(self, entity_id: str, schema: FormInstanceInSchema) -> FormInstanceSchema:
        form_instance = await self._update_by_id(schema, entity_id, is_partial=True)
        return form_instance.convert_to_schema()

    async def delete_form_instance(self, entity_id: str) -> None:
        await self.form_instance_assignment_repository.delete_by_instance_id(entity_id)
        return await self._delete_by_id(entity_id)

    async def create_form_instance(self, user_id: str, data_in: FormInstanceInSchema) -> FormInstanceSchema:
        form_instance = await self.repository.create(
            FormInstanceEntity(
                name=data_in.name,
                description=data_in.description,
                user_id=user_id,
                form_id=data_in.form_id,
                usage_type=data_in.usage_type,
            )
        )
        return form_instance.convert_to_schema()