from enum import Enum


class FormFieldTypeEnum(str, Enum):
    CHOICE = 'CHOICE'
    MULTI_CHOICE = 'MULTI_CHOICE'
    TEXT = 'TEXT'
    SHORT_TEXT = 'SHORT_TEXT'
    LONG_TEXT = 'LONG_TEXT'
    FILE = 'FILE'
    DATE = 'DATE'
    DATE_TIME = 'DATE_TIME'
    TIME = 'TIME'
    NUMBER = 'NUMBER'
