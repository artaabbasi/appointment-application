from pydantic import BaseModel

from common.lib.base_entity import BaseEntity
from common.lib.base_respository import BaseRepository
from common.lib.base_service import BaseService
from typing import TypeVar, List, Generic, Type, Optional
from common.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException
)
from common.lib.service_action_enum import ServiceActionEnum
from util.logger import Logger

T = TypeVar('T', bound=BaseEntity)
R = TypeVar('R', bound=BaseRepository)


class BaseCRUDService(BaseService, Generic[T, R]):
    _logger_instance: Logger

    def __init__(self,
                 repository_type: Type[R],
                 entity_type: Optional[Type[T]] = None,
                 action: Optional[ServiceActionEnum] = ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY,
                 not_found_code: str = 'NOT_FOUND',
                 bad_request_code: str = 'BAD_REQUEST'):

        super().__init__()
        self._logger_instance = None
        if action == ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY:
            self.repository = repository_type()
        else:
            self.repository = repository_type(entity_type)
        self.not_found_code = not_found_code
        self.bad_request_code = bad_request_code

    async def _create(self, entity: T) -> T:
        return await self.repository.create(entity)

    async def _count(self, filters: dict = None, search: str = None):
        if filters is None:
            filters = {}
        return await self.repository.count(filters, search)

    async def get_count(self, filters: dict = None, search: str = None) -> int:
        count = await self._count(filters, search)
        return count

    async def _update_by_id(self, data: BaseModel, entity_id: str, is_partial: bool = True) -> T:
        entity = await self.repository.fetch_by_id(entity_id)
        if not entity:
            raise NotFoundException(code=self.not_found_code)
        update_data = data.model_dump(exclude_unset=is_partial)
        for key, value in update_data.items():
            try:
                setattr(entity, key, value)
            except:
                raise BadRequestException(code=self.bad_request_code)
        return await self.repository.update(entity)

    async def _delete_by_id(self, entity_id: str) -> None:
        entity = await self.repository.fetch_by_id(entity_id)
        if not entity:
            raise NotFoundException(code=self.not_found_code)
        return await self.repository.delete(entity)

    async def _list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None, *, where_condition: Optional[list] = None) -> Optional[List[T]]:
        if filters is None:
            filters = {}
        return await self.repository.fetch_paginated_list_by_filters(page, size, filters, search, where_condition=where_condition)

    async def _get(self, entity_id: str) -> Optional[T]:
        return await self.repository.fetch_by_id(entity_id)
