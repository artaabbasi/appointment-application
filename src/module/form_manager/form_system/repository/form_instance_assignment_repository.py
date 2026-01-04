from typing import Optional, List

from sqlalchemy import select, and_, delete, desc, Select
from sqlalchemy.exc import NoResultFound, IntegrityError

from common.exceptions import NotFoundException, InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.form_manager.form_system.entity.form_instance_assignment_entity import FormInstanceAssignmentEntity
from module.form_manager.form_system.repository.form_instance_assignment_user_repository import \
    FormInstanceAssignmentUserRepository


class FormInstanceAssignmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormInstanceAssignmentEntity,
                         filter_fields=[FormInstanceAssignmentEntity.form_instance_id],
                         search_fields=[FormInstanceAssignmentEntity.name],
                         date_filters={
                             "release_from": (DateFilterEnum.FROM, FormInstanceAssignmentEntity.release_at),
                             "release_to": (DateFilterEnum.TO, FormInstanceAssignmentEntity.release_at),
                             "deadline_from": (DateFilterEnum.FROM, FormInstanceAssignmentEntity.deadline),
                             "deadline_to": (DateFilterEnum.TO, FormInstanceAssignmentEntity.deadline),
                         },
                         order_by=[desc(FormInstanceAssignmentEntity.created_at)])

    async def delete_by_instance_id(self, form_instance_id: str) -> None:
        try:
            async with get_session() as session:
                await session.execute(
                    delete(self.type)
                    .where(and_(FormInstanceAssignmentEntity.form_instance_id == form_instance_id))
                )
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def _get_queryset(self, q: Select, filters: dict, search: str = None, where: list = None, or_conditions: list = None, is_count: bool = False) -> Select:
        if where is None:
            where = []
        if 'assigned_user_id' in filters:
            entities = await FormInstanceAssignmentUserRepository().fetch_by_user_id(filters['assigned_user_id'])
            where.append(FormInstanceAssignmentEntity.id.in_([en.form_instance_assignment_id for en in entities]))
        q = await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
        return q
