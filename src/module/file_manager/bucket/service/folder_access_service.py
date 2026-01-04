import asyncio
from typing import Union, List

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.exceptions import NotFoundException, ForbiddenException
from common.file_manager.enum.folder_access_type import FolderAccessType
from common.file_manager.enum.folder_accesses_enum import FolderAccessesEnum
from common.file_manager.schema.folder_access_accesses_schema import FolderAccessAccessesSchema
from common.file_manager.schema.folder_access_in_schema import FolderAccessInSchema, FolderAccessInListSchema
from common.file_manager.schema.folder_access_schema import FolderAccessSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.account.authorization.service.role_service import RoleService
from module.account.user.service import CustomerService
from module.file_manager.bucket.entity.folder_access_entity import FolderAccessEntity
from module.file_manager.bucket.enum.error_code_enum import FileErrorCodeEnum
from module.file_manager.bucket.repository.folder_access_repository import FolderAccessRepository
from module.file_manager.bucket.repository.folder_repository import FolderRepository


class FolderAccessService(BaseCRUDService):
    def __init__(self):
        super().__init__(FolderAccessRepository, FolderAccessEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.folder_repository = FolderRepository()

    async def _aggregate_schema(self, schema: Union[FolderAccessSchema, list[FolderAccessSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema(item) for item in schema
                ]
            )
        else:
            if schema.type == FolderAccessType.USER:
                schema.instance = await CustomerService().get_not_detailed_user_by_id(schema.instance_id)
            elif schema.type == FolderAccessType.ROLE:
                try:
                    schema.instance = await RoleService().get_by_id(schema.instance_id)
                except NotFoundException:
                    pass
            schema.user = await CustomerService().get_not_detailed_user_by_id(schema.user_id)
        return schema

    async def get_folder_access_list(self,
                                     page: int = 1,
                                     size: int = 10,
                                     filters: dict = None,
                                     search: str = "") \
            -> list[FolderAccessSchema]:
        folder_accesses = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._aggregate_schema([folder_access.convert_to_schema() for folder_access in folder_accesses])

    async def get_by_id(self, folder_access_id: str) -> FolderAccessSchema:
        folder_access = await self.repository.fetch_by_id(folder_access_id)
        return await self._aggregate_schema(folder_access.convert_to_schema())

    async def get_by_user_id_and_folder_id(self, user_id: str, folder_id: str) -> FolderAccessAccessesSchema:
        folder_access = FolderAccessAccessesSchema()
        accesses = [access for access in FolderAccessesEnum
                    if await self.user_has_access_to_folder(access, user_id, folder_id)]
        folder_access.folder_id = folder_id
        folder_access.accesses = accesses
        return folder_access

    async def update_folder_access(self,
                                   user_id: str, staff_role: AdminRolesEnum,
                                   entity_id: str,
                                   schema: FolderAccessSchema) -> FolderAccessSchema:
        folder_access = await self.repository.fetch_by_id(entity_id)
        if staff_role == AdminRolesEnum.supporter:
            if not await self.user_has_access_to_folder(
                    FolderAccessesEnum.CREATE_FOLDER,
                    user_id,
                    folder_access.folder_id
            ):
                raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
        folder_access = await self._update_by_id(schema, entity_id, is_partial=True)
        return await self._aggregate_schema(folder_access.convert_to_schema())

    async def delete_folder_access(self,
                                   user_id: str, staff_role: AdminRolesEnum,
                                   entity_id: str) -> None:
        folder_access = await self.repository.fetch_by_id(entity_id)
        if staff_role == AdminRolesEnum.supporter:
            if not await self.user_has_access_to_folder(
                    FolderAccessesEnum.CREATE_FOLDER,
                    user_id,
                    folder_access.folder_id
            ):
                raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
        return await self._delete_by_id(entity_id)

    async def create_folder_access(self,
                                   user_id: str,
                                   staff_role: AdminRolesEnum,
                                   data_in: FolderAccessInListSchema) -> List[FolderAccessSchema]:
        folder_accesses = []
        for datum in data_in.data:
            if staff_role == AdminRolesEnum.supporter:
                if not await self.user_has_access_to_folder(
                        FolderAccessesEnum.CREATE_FOLDER,
                        user_id,
                        datum.folder_id
                ):
                    raise ForbiddenException(FileErrorCodeEnum.FOLDER_NOT_FOR_USER)
            folder_access = await self.repository.get_by_instance_id_and_folder_id(instance_id=datum.instance_id,
                                                                                   type=datum.type,
                                                                                   folder_id=datum.folder_id
                                                                                   )
            if folder_access is not None:
                await self.repository.delete(folder_access)
            folder_access = await self.repository.create(
                FolderAccessEntity(
                    type=datum.type,
                    instance_id=datum.instance_id,
                    folder_id=datum.folder_id,
                    accesses=datum.accesses,
                    user_id=user_id
                )
            )
            folder_accesses.append(folder_access)
        return await self._aggregate_schema([folder_access.convert_to_schema() for folder_access in folder_accesses])

    async def get_folder_ids_for_user(self, user_id: str) -> list[str]:
        folder_ids = []
        user_folder_accesses = await self.repository.get_by_instance_id(user_id,
                                                                        FolderAccessType.USER)
        folder_ids.extend([folder_access.folder_id for folder_access in user_folder_accesses])
        user_roles = await RoleService().get_user_roles(user_id)
        for role in user_roles:
            role_folder_accesses = await self.repository.get_by_instance_id(role.id,
                                                                            FolderAccessType.ROLE)
            folder_ids.extend([folder_access.folder_id for folder_access in role_folder_accesses])
        return folder_ids

    async def user_has_access_to_folder(self, access: FolderAccessesEnum, user_id: str, folder_id: str) -> bool:
        try:
            folder_entity = await self.folder_repository.fetch_by_id(folder_id)
        except NotFoundException:
            folder_entity = None
        folder_access = await self.repository.get_by_instance_id_and_folder_id(user_id,
                                                                               FolderAccessType.USER,
                                                                               folder_id)
        if folder_access is None:
            user_roles = await RoleService().get_user_roles(user_id)
            for role in user_roles:
                folder_access = await self.repository.get_by_instance_id_and_folder_id(role.id,
                                                                                       FolderAccessType.ROLE,
                                                                                       folder_id)
                if folder_access is not None:
                    break
        else:
            if folder_access.accesses is not None:
                if access in folder_access.accesses:
                    return True
        if getattr(folder_entity, 'parent_folder_id', None) is not None:
            return await self.user_has_access_to_folder(access, user_id, folder_entity.parent_folder_id)
        return False
