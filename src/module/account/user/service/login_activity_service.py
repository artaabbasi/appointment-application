import asyncio
from typing import Optional, List

from common.account.schema.login_activity_schema import LoginActivitySchema
from common.exceptions import NotFoundException
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.account.user.entity.login_activity_entity import LoginActivityEntity
from module.account.user.repository.login_activity_repository import LoginActivityRepository
from module.account.user.util.redis_jwt_util import RedisJwtUtil
from util.timestamp import DatetimeUtil
from sqlalchemy.exc import MultipleResultsFound


class LoginActivityService(BaseCRUDService):

    def __init__(self):
        super().__init__(LoginActivityRepository, LoginActivityEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def create_login_activity(self, user_id: str, token: str, expire_timestamp: int,
                                    ip_address: Optional[str] = None,
                                    agent: Optional[str] = None) -> LoginActivitySchema:
        login_activity = await self._create(LoginActivityEntity(
            user_id=user_id,
            refresh_token=token,
            expire_timestamp=expire_timestamp,
            ip_address=ip_address,
            agent=agent,
        ))
        return login_activity.convert_to_schema()

    async def logout(self, user_id: str, token: str) -> LoginActivitySchema:
        try:
            login_activity = await self.repository.fetch_by_user_id_and_token(user_id, token)
        except NotFoundException:
            login_activity = await self._create(LoginActivityEntity(
                user_id=user_id,
                refresh_token=token,
                expire_timestamp=int(DatetimeUtil.utc_now_timestamp())
            ))
        login_activity.expire_timestamp = int(DatetimeUtil.utc_now_timestamp())
        await RedisJwtUtil().blacklist_token(token)
        await self.repository.update(login_activity)
        return login_activity.convert_to_schema()

    async def logout_by_activity_id(self, user_id: str, activity_id: str) -> LoginActivitySchema:
        login_activity = await self.repository.fetch_by_id_and_user_id(activity_id, user_id)
        login_activity.expire_timestamp = int(DatetimeUtil.utc_now_timestamp())
        await RedisJwtUtil().blacklist_token(login_activity.refresh_token)
        await self.repository.update(login_activity)
        return login_activity.convert_to_schema()

    async def logout_others_by_refresh_token(self, user_id: str, refresh_token: str) -> List[LoginActivitySchema]:
        login_activities = await self.repository.exclude_by_user_id_and_token(user_id, refresh_token)
        for login_activity in login_activities:
            login_activity.expire_timestamp = int(DatetimeUtil.utc_now_timestamp())
            await RedisJwtUtil().blacklist_token(login_activity.refresh_token)
            await self.repository.update(login_activity)
        return [login_activity.convert_to_schema() for login_activity in login_activities]

    async def refresh_token(self, user_id: str, token: str, new_token: str, new_timestamp: int) -> LoginActivitySchema:
        try:
            login_activity = await self.repository.fetch_by_user_id_and_token(user_id, token)
        except NotFoundException:
            login_activity = await self._create(LoginActivityEntity(
                user_id=user_id,
                refresh_token=new_token,
                expire_timestamp=new_timestamp
            ))
        except MultipleResultsFound:
            login_activities = await self.repository.fetch_all_by_user_id_and_token(user_id, token)
            await asyncio.gather(*[self.logout_by_activity_id(user_id, login_activity.id) for login_activity in login_activities])
            login_activity = await self._create(LoginActivityEntity(
                user_id=user_id,
                refresh_token=new_token,
                expire_timestamp=new_timestamp
            ))
        login_activity.expire_timestamp = new_timestamp
        login_activity.refresh_token = new_token
        await RedisJwtUtil().blacklist_token(token)
        await self.repository.update(login_activity)
        return login_activity.convert_to_schema()

    async def get_login_activities(self, user_id: str,
                                   is_active: Optional[bool] = True,
                                   refresh_token: Optional[str] = None) -> List[LoginActivitySchema]:
        login_activities = await self._list(1, -1, {"is_active": is_active, LoginActivityEntity.user_id: user_id})
        return [login_activity.convert_to_schema(refresh_token) for login_activity in login_activities]
