from enum import Enum


class FolderAccessType(str, Enum):
    ROLE = "ROLE"
    USER = "USER"
    