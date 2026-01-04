from enum import Enum


class AdminRolesEnum(str, Enum):
    owner_admin = 'owner-admin'
    admin = 'admin'
    full_read = 'full_read'
    supporter = 'supporter'
