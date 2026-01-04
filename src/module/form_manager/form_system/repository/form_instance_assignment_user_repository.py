from typing import Optional, List

from sqlalchemy import select, and_, desc, Select
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_system.entity.form_instance_assignment_user_entity import FormInstanceAssignmentUserEntity


class FormInstanceAssignmentUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormInstanceAssignmentUserEntity,
                         filter_fields=[FormInstanceAssignmentUserEntity.user_id,
                                        FormInstanceAssignmentUserEntity.form_instance_assignment_id,
                                        FormInstanceAssignmentUserEntity.assigned_from_role_id,
                                        FormInstanceAssignmentUserEntity.user_form_id],
                         order_by=[desc(FormInstanceAssignmentUserEntity.created_at)])


    async def fetch_by_user_id(
            self,
            user_id: str,
    ) -> List[FormInstanceAssignmentUserEntity]:
        q = select(FormInstanceAssignmentUserEntity)
        q = q.filter(and_(FormInstanceAssignmentUserEntity.user_id == user_id))
        async with get_session() as session:
            result = await session.execute(q)
            entities = result.scalars().all()
        return entities

    async def fetch_assigned_role_ids_by_form_instance_assignment_id(
            self,
            form_instance_assignment_id: str,
    ) -> List[str]:
        q = select(FormInstanceAssignmentUserEntity.assigned_from_role_id)
        q = q.filter(and_(FormInstanceAssignmentUserEntity.form_instance_assignment_id == form_instance_assignment_id))
        q = q.distinct()
        async with get_session() as session:
            result = await session.execute(q)
            role_ids = result.scalars().all()
        return role_ids

    async def fetch_by_user_id_and_form_instance_assignment_id(
            self,
            user_id: str,
            form_instance_assignment_id: str,
    ) -> Optional[FormInstanceAssignmentUserEntity]:
        q = select(FormInstanceAssignmentUserEntity)
        q = q.filter(and_(FormInstanceAssignmentUserEntity.user_id == user_id,
                          FormInstanceAssignmentUserEntity.form_instance_assignment_id == form_instance_assignment_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND, form_instance_assignment_id)
        return entity

    async def _get_queryset(self, q: Select, filters: dict, search: str = None, where: list = None, or_conditions: list = None, is_count: bool = False) -> Select:
        if filters.get('user_form_id_is_null') is not None:
            if filters['user_form_id_is_null']:
                where = [FormInstanceAssignmentUserEntity.user_form_id.is_(None)]
            else:
                where = [FormInstanceAssignmentUserEntity.user_form_id.is_not(None)]
        q = await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
        return q
