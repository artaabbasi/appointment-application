import asyncio

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.account.schema.profile_update_schema import ProfileUpdateSchema
from common.account.schema.user_schema import CustomerUserSchema
from common.exceptions import NotFoundException
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.user_entity import UserEntity
from ..repository.profile_repository import ProfileRepository
from ..repository.user_repository import UserRepository
from typing import List, Optional
import io


class CustomerService(BaseCRUDService):

    def __init__(self):
        super().__init__(UserRepository, UserEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.profile_repository = ProfileRepository()

    async def _get_detailed_users(self, users: List[UserEntity]) -> List[CustomerUserSchema]:
        result = []
        for user in users:
            profile = await self.profile_repository.fetch_by_id(user.profile_id)
            customer_profile = CustomerUserSchema.load_from_entity(user,
                                                                   profile)
            result.append(customer_profile)

        return result

    async def get_not_detailed_user_by_id(self, user_id: str) -> Optional[NotDetailedUserSchema]:
        try:
            user = await self.repository.fetch_by_id(user_id)
        except NotFoundException:
            return None
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        customer_profile = NotDetailedUserSchema.load_from_entity(user,
                                                                  profile)

        return customer_profile

    async def get_not_detailed_users_by_ids(self, user_ids: List[str]) -> List[NotDetailedUserSchema]:
        customer_profiles = []
        users = await self.repository.fetch_all_by_ids(user_ids)
        profiles = await self.profile_repository.fetch_all_by_ids([user.profile_id for user in users])
        for user in users:
            for profile in profiles:
                if user.profile_id == profile.id:
                    customer_profiles.append(NotDetailedUserSchema.load_from_entity(user, profile))
                    profiles.remove(profile)
                    break
        return customer_profiles

    async def get_user_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[CustomerUserSchema]:
        users = await self._list(page, size, filters, search)
        return await self._get_detailed_users(users)

    async def update_user(self, user_id: str, user_schema: ProfileUpdateSchema) -> CustomerUserSchema:
        user = await self.repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)

        profile.first_name = user_schema.first_name if user_schema.first_name else profile.first_name
        profile.last_name = user_schema.last_name if user_schema.last_name else profile.last_name
        profile.national_code = user_schema.national_code if user_schema.national_code else profile.national_code
        profile.birth_date = user_schema.birth_date if user_schema.birth_date else profile.birth_date
        profile.father_name = user_schema.father_name if user_schema.father_name else profile.father_name

        user.avatar = user_schema.avatar if user_schema.avatar else user.avatar

        await asyncio.gather(
            self.repository.update(user),
            self.profile_repository.update(profile)
        )
        return CustomerUserSchema.load_from_entity(user, profile)

    async def delete_user(self, user_id: str) -> None:
        user = await self.repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)

        await asyncio.gather(
            self.repository.delete(user),
            self.profile_repository.delete(profile)
        )
        return
