from enum import Enum


class DepositTypeEnum(str, Enum):
    ABSOLUTE = "ABSOLUTE"
    PERCENT = "PERCENT"
