import asyncio

from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.api_key_schema import ApiKeyUserSchema
from common.account.schema.api_key_user_create_schema import ApiKeyUserCreateSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from .login_activity_service import LoginActivityService
from ..entity.user_entity import UserEntity
from ..entity.profile_entity import ProfileEntity
from ..repository.profile_repository import ProfileRepository
from ..repository.user_repository import UserRepository
from typing import List, Union
from ..util.password_util import get_password_hash


class ApiKeyUserService(BaseCRUDService):

    def __init__(self):
        super().__init__(UserRepository, UserEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.profile_repository = ProfileRepository()

    async def _get_detailed_user(self, user: UserEntity) -> ApiKeyUserSchema:
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        admin_profile = ApiKeyUserSchema.load_from_entity(user, profile)
        return admin_profile

    async def _get_detailed_users(self, users: List[UserEntity]) -> List[ApiKeyUserSchema]:
        result = []
        for user in users:
            admin_profile = await self._get_detailed_user(user)
            result.append(admin_profile)
        return result

    async def get_user_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[ApiKeyUserSchema]:
        if filters is None:
            filters = {}
        users = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._get_detailed_users(users)

    async def get_user_by_id(self, user_id: str) -> ApiKeyUserSchema:
        user = await self.repository.fetch_by_id(user_id)
        return await self._get_detailed_user(user)

    async def create_user(self, user_schema: ApiKeyUserCreateSchema) -> ApiKeyUserSchema:
        profile = await self.profile_repository.create(
            ProfileEntity(
                phone_number=user_schema.phone_number,
                first_name=user_schema.first_name,
                last_name=user_schema.last_name,
                email=user_schema.email,
                birth_date=user_schema.birth_date,
                national_code=user_schema.national_code,
            )
        )

        user = await self.repository.create(
            UserEntity(
                profile_id=profile.id,
                username=user_schema.username,
                password=get_password_hash(user_schema.password),
                group=UserGroupEnum.api_key,
                is_active=user_schema.is_active,
                is_verified=True
            )
        )

        return ApiKeyUserSchema.load_from_entity(user, profile)

    async def update_user(self, user_id: str, user_schema: ApiKeyUserCreateSchema) \
            -> ApiKeyUserSchema:
        user = await self.repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)

        profile.phone_number = user_schema.phone_number if user_schema.phone_number is not None  else profile.phone_number
        profile.first_name = user_schema.first_name if user_schema.first_name is not None  else profile.first_name
        profile.last_name = user_schema.last_name if user_schema.last_name is not None  else profile.last_name
        profile.email = user_schema.email if user_schema.email is not None  else profile.email
        profile.birth_date = user_schema.birth_date if user_schema.birth_date is not None  else profile.birth_date
        profile.national_code = user_schema.national_code if user_schema.national_code is not None  else profile.national_code
        user.avatar = user_schema.avatar if user_schema.avatar is not None  else user.avatar
        user.username = user_schema.username if user_schema.username is not None  else user.username
        user.is_active = user_schema.is_active if user_schema.is_active is not None else user.is_active

        await asyncio.gather(
            self.repository.update(user),
            self.profile_repository.update(profile)
        )
        return ApiKeyUserSchema.load_from_entity(user, profile)

    async def delete_user(self, user_id: str) -> None:
        user = await self.repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)

        await asyncio.gather(
            self.repository.delete(user),
            self.profile_repository.delete(profile),
        )
        return

    async def change_admin_password(self, user_id: str, password: str) -> None:
        user = await self.repository.fetch_by_id(user_id)
        user.password = get_password_hash(password)
        await self.repository.update(user)
        await LoginActivityService().logout_others_by_refresh_token(user_id, "")
