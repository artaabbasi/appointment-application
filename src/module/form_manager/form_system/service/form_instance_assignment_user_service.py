import asyncio
import io
from typing import List, Union, Optional

from sqlalchemy.util import await_only

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.account.schema.role_schema import RoleSchema
from common.exceptions import NotFoundException
from common.form_manager.schema.form_instance_assignment_user_answer_in_schema import \
    FormInstanceAssignmentUserAnswerInSchema
from common.form_manager.schema.form_instance_assignment_user_in_schema import FormInstanceAssignmentUserInSchema
from common.form_manager.schema.form_instance_assignment_user_schema import FormInstanceAssignmentUserSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.account.authorization.service.role_service import RoleService
from module.account.user.service import CustomerService
from module.form_manager.form_manager.service.form_service import FormService
from module.form_manager.form_system.entity.form_instance_assignment_user_entity import FormInstanceAssignmentUserEntity
from module.form_manager.form_system.repository.form_instance_assignment_repository import \
    FormInstanceAssignmentRepository
from module.form_manager.form_system.repository.form_instance_assignment_user_repository import FormInstanceAssignmentUserRepository
from module.form_manager.form_system.repository.form_instance_repository import FormInstanceRepository
from util.timestamp import DatetimeUtil


class FormInstanceAssignmentUserService(BaseCRUDService):
    def __init__(self):
        super().__init__(FormInstanceAssignmentUserRepository, FormInstanceAssignmentUserEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.form_instance_assignment_repository = FormInstanceAssignmentRepository()
        self.form_instance_repository = FormInstanceRepository()

    async def _aggregate_schema(self, schema: Union[FormInstanceAssignmentUserSchema, list[FormInstanceAssignmentUserSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema(item) for item in schema
                ]
            )
        else:
            try:
                schema.user = await CustomerService().get_not_detailed_user_by_id(schema.user_id)
            except NotFoundException:
                pass
            try:
                schema.assigned_from_role = await RoleService().get_not_detailed_by_id(schema.assigned_from_role_id)
            except NotFoundException:
                pass
        return schema

    async def get_form_instance_assignment_user_list(self,
                                    page: int = 1,
                                    size: int = 10,
                                    filters: dict = None,
                                    search: str = "") \
            -> list[FormInstanceAssignmentUserSchema]:
        form_instance_assignment_users = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._aggregate_schema([form_instance_assignment_user.convert_to_schema() for form_instance_assignment_user in form_instance_assignment_users])

    async def form_instance_assignment_user_list_excel_export(self,
                                                              form_instance_assignment_id: str,
                                                              filters: dict = None,
                                                              search: str = "") -> io.BytesIO:
        if filters is None:
            filters = {}
        filters.update({FormInstanceAssignmentUserEntity.form_instance_assignment_id: form_instance_assignment_id})
        form_instance_assignment_users = await self.repository.fetch_paginated_list_by_filters(1, -1, filters, search)
        form_instance_assignment = await self.form_instance_assignment_repository.fetch_by_id(form_instance_assignment_id)
        form_instance = await self.form_instance_repository.fetch_by_id(form_instance_assignment.form_instance_id)
        return await FormService().get_user_form_excel_by_ids(
            form_instance.form_id,
            [form_instance_assignment_user.user_form_id for form_instance_assignment_user in
            form_instance_assignment_users if form_instance_assignment_user.user_form_id is not None],
        )

    async def get_by_id(self, form_instance_assignment_user_id: str) -> FormInstanceAssignmentUserSchema:
        form_instance_assignment_user = await self.repository.fetch_by_id(form_instance_assignment_user_id)
        return await self._aggregate_schema(form_instance_assignment_user.convert_to_schema())

    async def update_form_instance_assignment_user(self, entity_id: str, schema: FormInstanceAssignmentUserInSchema) -> FormInstanceAssignmentUserSchema:
        form_instance_assignment_user = await self._update_by_id(schema, entity_id, is_partial=True)
        return form_instance_assignment_user.convert_to_schema()

    async def delete_form_instance_assignment_user(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_form_instance_assignment_user(self, data_in: FormInstanceAssignmentUserInSchema) -> FormInstanceAssignmentUserSchema:
        try:
            form_instance_assignment_user = await self.repository.fetch_by_user_id_and_form_instance_assignment_id(data_in.user_id,
                                                                                                                   data_in.form_instance_assignment_id)
        except NotFoundException:
            form_instance_assignment_user = await self.repository.create(
                FormInstanceAssignmentUserEntity(
                    user_id=data_in.user_id,
                    assigned_from_role_id=data_in.assigned_from_role_id,
                    form_instance_assignment_id=data_in.form_instance_assignment_id,
                    user_form_id=data_in.user_form_id,
                )
            )
        return form_instance_assignment_user.convert_to_schema()

    async def assign_instance_to_users(self,
                                        form_instance_assignment_id: str,
                                        user_ids: Optional[List[str]] = None,
                                        assigned_from_role_id: Optional[str] = None):
        if user_ids is None:
            return
        for user_id in user_ids:
            await self.create_form_instance_assignment_user(
                FormInstanceAssignmentUserInSchema(
                    user_id=user_id,
                    assigned_from_role_id=assigned_from_role_id,
                    form_instance_assignment_id=form_instance_assignment_id
                )
            )

    async def assign_instance_to_roles(self,
                                        form_instance_assignment_id: str,
                                        role_ids: Optional[List[str]] = None):
        if role_ids is None:
            return
        for role_id in role_ids:
            user_ids = await RoleService().get_user_ids_by_role_id(role_id=role_id)
            await self.assign_instance_to_users(form_instance_assignment_id, user_ids, role_id)

    async def create_multi_form_instance_assignment_users(self,
                                                          form_instance_assignment_id: str,
                                                          assign_to_user_ids: Optional[List[str]] = None,
                                                          assign_to_role_ids: Optional[List[str]] = None):
        await asyncio.gather(
            self.assign_instance_to_users(form_instance_assignment_id, assign_to_user_ids),
            self.assign_instance_to_roles(form_instance_assignment_id, assign_to_role_ids)
        )
        return None

    async def get_by_user_id_and_form_instance_assignment_id(self, user_id: str, form_instance_assignment_id: str) \
            -> FormInstanceAssignmentUserSchema:
        form_instance_assignment_user = await self.repository.fetch_by_user_id_and_form_instance_assignment_id(user_id,
                                                                                                               form_instance_assignment_id)
        return await self._aggregate_schema(form_instance_assignment_user.convert_to_schema())

    async def update_by_user_id_and_form_instance_assignment_id(self, user_id: str, form_instance_assignment_id: str,
                                                                schema: FormInstanceAssignmentUserAnswerInSchema) \
            -> FormInstanceAssignmentUserSchema:
        _form_instance_assignment_user = await self.repository.fetch_by_user_id_and_form_instance_assignment_id(user_id,
                                                                                                               form_instance_assignment_id)
        form_instance_assignment_user = await self._update_by_id(schema, _form_instance_assignment_user.id, is_partial=True)
        return form_instance_assignment_user.convert_to_schema()

    async def get_assigned_roles_by_form_instance_assignment_id(self, form_instance_assignment_id: str) -> List[RoleSchema]:
        role_ids = await self.repository.fetch_assigned_role_ids_by_form_instance_assignment_id(form_instance_assignment_id)
        roles = await RoleService().get_by_ids(role_ids)
        return roles