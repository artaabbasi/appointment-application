import asyncio

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.admin_change_profile_schema import AdminChangeProfileSchema
from common.account.schema.admin_create_schema import AdminCreateSchema
from common.account.schema.admin_register_schema import AdminRegisterSchema
from common.account.schema.admin_schema import AdminUserSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from .login_activity_service import LoginActivityService
from ..entity.user_entity import UserEntity
from ..entity.profile_entity import ProfileEntity
from ..entity.staff_entity import StaffEntity
from ..repository.profile_repository import ProfileRepository
from ..repository.staff_repository import StaffRepository
from ..repository.user_repository import UserRepository
from typing import List, Union

from ..util.password_util import get_password_hash
from ...authorization.repository.user_role_repository import UserRoleRepository
from ...authorization.service.role_service import RoleService


class AdminService(BaseCRUDService):

    def __init__(self):
        super().__init__(UserRepository, UserEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.profile_repository = ProfileRepository()
        self.staff_repository = StaffRepository()
        self.user_role_repository = UserRoleRepository()

    async def _get_detailed_user(self, user: UserEntity) -> AdminUserSchema:
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        staff = await self.staff_repository.fetch_by_user_id(user.id)
        user_roles = await RoleService().get_user_roles(user.id)
        admin_profile = AdminUserSchema.load_from_entity(user, profile, staff, user_roles=user_roles)
        return admin_profile

    async def _get_detailed_users(self, users: List[UserEntity]) -> List[AdminUserSchema]:
        result = []
        for user in users:
            admin_profile = await self._get_detailed_user(user)
            result.append(admin_profile)
        return result

    async def get_user_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[AdminUserSchema]:
        if filters is None:
            filters = {}
        users = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._get_detailed_users(users)

    async def get_user_by_id(self, user_id: str) -> AdminUserSchema:
        user = await self.repository.fetch_by_id(user_id)
        return await self._get_detailed_user(user)

    async def create_user(self, user_schema: AdminCreateSchema) -> AdminUserSchema:
        profile = await self.profile_repository.create(
            ProfileEntity(
                phone_number=user_schema.phone_number,
                first_name=user_schema.first_name,
                en_first_name=user_schema.en_first_name,
                last_name=user_schema.last_name,
                en_last_name=user_schema.en_last_name,
                national_code=user_schema.national_code,
                internal_tel=user_schema.internal_tel,
                agent_code=user_schema.agent_code,
                branch_code=user_schema.branch_code,
            )
        )

        user = await self.repository.create(
            UserEntity(
                profile_id=profile.id,
                username=user_schema.username,
                password=get_password_hash(user_schema.password),
                group=UserGroupEnum.admin,
                is_verified=True
            )
        )

        staff = await self.staff_repository.create(
            StaffEntity(
                user_id=user.id,
                role=user_schema.role
            )
        )

        return AdminUserSchema.load_from_entity(user, profile, staff)

    async def update_user(self, user_id: str, user_schema: Union[AdminRegisterSchema, AdminChangeProfileSchema]) \
            -> AdminUserSchema:
        user = await self.repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        staff = await self.staff_repository.fetch_by_user_id(user.id)

        profile.phone_number = user_schema.phone_number if user_schema.phone_number else profile.phone_number
        profile.first_name = user_schema.first_name if user_schema.first_name else profile.first_name
        profile.last_name = user_schema.last_name if user_schema.last_name else profile.last_name
        profile.en_first_name = user_schema.en_first_name if user_schema.en_first_name else profile.en_first_name
        profile.en_last_name = user_schema.en_last_name if user_schema.en_last_name else profile.en_last_name
        profile.national_code = user_schema.national_code if user_schema.national_code else profile.national_code
        profile.internal_tel = user_schema.internal_tel if user_schema.internal_tel else profile.internal_tel
        profile.email = user_schema.email if user_schema.email else profile.email
        profile.birth_date = user_schema.birth_date if user_schema.birth_date else profile.birth_date
        profile.agent_code = user_schema.agent_code if user_schema.agent_code else profile.agent_code
        profile.branch_code = user_schema.branch_code if user_schema.branch_code else profile.branch_code

        user.avatar = user_schema.avatar if user_schema.avatar else user.avatar
        user.username = user_schema.username if user_schema.username else user.username
        if isinstance(user_schema, AdminRegisterSchema):
            staff.role = user_schema.role if user_schema.role else staff.role
            user.must_change_password = user_schema.must_change_password if user_schema.must_change_password is not None else user.must_change_password
            user.is_active = user_schema.is_active if user_schema.is_active is not None else user.is_active
            user.has_completed_profile = user_schema.has_completed_profile if user_schema.has_completed_profile is not None else user.has_completed_profile
        else:
            user.has_completed_profile = True
        await asyncio.gather(
            self.repository.update(user),
            self.staff_repository.update(staff),
            self.profile_repository.update(profile)
        )
        return AdminUserSchema.load_from_entity(user, profile, staff)

    async def delete_user(self, user_id: str) -> None:
        user = await self.repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        staff = await self.staff_repository.fetch_by_user_id(user.id)

        await asyncio.gather(
            self.repository.delete(user),
            self.staff_repository.delete(staff),
            self.profile_repository.delete(profile),
            self.user_role_repository.delete_by_user_id(user_id)
        )
        return

    async def change_admin_password(self, user_id: str, password: str) -> None:
        user = await self.repository.fetch_by_id(user_id)
        user.password = get_password_hash(password)
        await self.repository.update(user)
        await LoginActivityService().logout_others_by_refresh_token(user_id, "")

    async def migrate_admin_users(self):
        supp_users = await self.repository.fetch_paginated_list_by_filters(page=1,
                                                                           size=-1,
                                                                           filters={
                                                                               StaffEntity.role: AdminRolesEnum.supporter,
                                                                           })
        for user in supp_users:
            if user.last_login_at is None:
                user.password = get_password_hash(user.username)
                await self.repository.update(user)
