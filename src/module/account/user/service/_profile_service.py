from common.lib.base_service import BaseService
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.repository.profile_repository import ProfileRepository


class ProfileService(BaseService):

    def __init__(self):
        self.profile_repository = ProfileRepository()

    async def add_profile(self, phone_number: str) -> ProfileEntity:
        return await self.profile_repository.create(
            ProfileEntity(
                phone_number=phone_number
            )
        )
