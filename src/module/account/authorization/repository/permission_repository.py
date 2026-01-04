from common.lib.base_respository import BaseRepository
from module.account.authorization.entity.permission_entity import PermissionEntity


class PermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(PermissionEntity,
                         order_by=[PermissionEntity.module])
