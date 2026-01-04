import asyncio
from typing import List, Optional, Union

from common.exceptions import NotFoundException
from common.form_manager.schema.form_instance_assignment_in_schema import FormInstanceAssignmentInSchema
from common.form_manager.schema.form_instance_assignment_schema import FormInstanceAssignmentSchema
from common.form_manager.schema.form_instance_assignment_user_in_schema import FormInstanceAssignmentUserInSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.account.authorization.service.role_service import RoleService
from module.form_manager.form_system.entity.form_instance_assignment_entity import FormInstanceAssignmentEntity
from module.form_manager.form_system.entity.form_instance_assignment_user_entity import FormInstanceAssignmentUserEntity
from module.form_manager.form_system.repository.form_instance_assignment_repository import FormInstanceAssignmentRepository
from module.form_manager.form_system.service.form_instance_assignment_user_service import \
    FormInstanceAssignmentUserService
from module.form_manager.form_system.service.form_instance_service import FormInstanceService
from util.timestamp import DatetimeUtil


class FormInstanceAssignmentService(BaseCRUDService):
    def __init__(self):
        super().__init__(FormInstanceAssignmentRepository, FormInstanceAssignmentEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.form_instance_assignment_user_service = FormInstanceAssignmentUserService()

    async def _aggregate_schema(self, schema: Union[FormInstanceAssignmentSchema, list[FormInstanceAssignmentSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema(item) for item in schema
                ]
            )
        else:
            form_instance = await FormInstanceService().get_by_id(schema.form_instance_id)
            schema.form_instance = form_instance
            schema.users_count = await self.form_instance_assignment_user_service.get_count(
                {FormInstanceAssignmentUserEntity.form_instance_assignment_id: schema.id})
            schema.answered_users_count = await self.form_instance_assignment_user_service.get_count(
                {FormInstanceAssignmentUserEntity.form_instance_assignment_id: schema.id,
                 "user_form_id_is_null": False})
            schema.not_answered_users_count = await self.form_instance_assignment_user_service.get_count(
                {FormInstanceAssignmentUserEntity.form_instance_assignment_id: schema.id,
                 "user_form_id_is_null": True})
        return schema

    async def _aggregate_schema_for_user(self,
                                user_id: str,
                                schema: Union[FormInstanceAssignmentSchema, list[FormInstanceAssignmentSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema_for_user(user_id, item) for item in schema
                ]
            )
        else:
            form_instance = await FormInstanceService().get_by_id(schema.form_instance_id)
            schema.form_instance = form_instance
            schema.user_has_answer = bool(await self.form_instance_assignment_user_service.get_count(
                {FormInstanceAssignmentUserEntity.form_instance_assignment_id: schema.id,
                 "user_form_id_is_null": False, FormInstanceAssignmentUserEntity.user_id: user_id}))
        return schema

    async def get_form_instance_assignment_list(self,
                                    page: int = 1,
                                    size: int = 10,
                                    filters: dict = None,
                                    search: str = "") \
            -> list[FormInstanceAssignmentSchema]:
        form_instance_assignments = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._aggregate_schema([form_instance_assignment.convert_to_schema() for form_instance_assignment in form_instance_assignments])

    async def get_form_instance_assignment_list_for_user(self,
                                                        user_id: str,
                                                        page: int = 1,
                                                        size: int = 10,
                                                        filters: dict = None,
                                                        search: str = "") \
            -> list[FormInstanceAssignmentSchema]:
        if filters is None:
            filters = {}
        filters.update({"assigned_user_id": user_id})
        form_instance_assignments = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._aggregate_schema_for_user(user_id, [form_instance_assignment.convert_to_schema() for form_instance_assignment in form_instance_assignments])

    async def get_by_id(self, form_instance_assignment_id: str) -> FormInstanceAssignmentSchema:
        form_instance_assignment = await self.repository.fetch_by_id(form_instance_assignment_id)
        return await self._aggregate_schema(form_instance_assignment.convert_to_schema())

    async def get_by_ids(self, form_instance_assignment_ids: List[str]) -> List[FormInstanceAssignmentSchema]:
        form_instance_assignments = await self.repository.fetch_all_by_ids(form_instance_assignment_ids)
        return [form_instance_assignment.convert_to_schema() for form_instance_assignment in form_instance_assignments]

    async def update_form_instance_assignment(self, entity_id: str, schema: FormInstanceAssignmentInSchema) -> FormInstanceAssignmentSchema:
        form_instance_assignment = await self._update_by_id(schema, entity_id, is_partial=True)
        return form_instance_assignment.convert_to_schema()

    async def delete_form_instance_assignment(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_form_instance_assignment(self, user_id: str, data_in: FormInstanceAssignmentInSchema) -> FormInstanceAssignmentSchema:
        form_instance_assignment = await self.repository.create(
            FormInstanceAssignmentEntity(
                name=data_in.name,
                user_id=user_id,
                form_instance_id=data_in.form_instance_id,
                release_at=data_in.release_at,
                deadline=data_in.deadline,
            )
        )
        await self.form_instance_assignment_user_service.create_multi_form_instance_assignment_users(form_instance_assignment.id,
                                                                                                     data_in.assign_to_user_ids,
                                                                                                     data_in.assign_to_role_ids)
        return form_instance_assignment.convert_to_schema()