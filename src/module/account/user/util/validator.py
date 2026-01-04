import re
from abc import ABC, abstractmethod
from fastapi import HTTPException

from common.exceptions import BadRequestException

from module.user.enum.error_code_enum import ErrorCodeEnum


class IValidator(ABC):
    @abstractmethod
    def validate(self, value: str):
        """Concrete classes must raise subclasses of `fastapi.HttpException` at their validate method."""


class PasswordValidator(IValidator):
    def __init__(self):
        self.capital_case_regex_str = r".*[A-Z].*"
        self.capital_case_complied_regex = re.compile(self.capital_case_regex_str)
        self.lowercase_case_regex_str = r".*[a-z].*"
        self.lowercase_case_complied_regex = re.compile(self.lowercase_case_regex_str)
        self.special_chars_regex_str = r".*[\s!\"#$%&'()*+,-./:;<=>?@\[\]^_`{|}~].*"
        self.special_chars_complied_regex = re.compile(self.special_chars_regex_str)

    def validate(self, password: str) -> None:
        password = password.strip()
        if not (
                (self.capital_case_complied_regex.match(password) or
                 self.lowercase_case_complied_regex.match(password)) and
                self.special_chars_complied_regex.match(password) and
                8 <= len(password) <= 128
        ):
            raise BadRequestException(ErrorCodeEnum.INVALID_PASSWORD,
                                      " Password must be at least 8 characters long"
                                      " and contain at least one letter and special characters.")


class PhoneNumberValidator(IValidator):
    def __init__(self):
        self.phone_number_regex = r'^\+?\d+(-\d+)*$'
        self.re = re.compile(self.phone_number_regex)

    def validate(self, phone_number: str) -> None:
        if not phone_number:
            return
        phone_number = phone_number.strip()
        if (len(phone_number) < 9 or len(phone_number) > 13) or not bool(self.re.match(phone_number)):
            raise BadRequestException(ErrorCodeEnum.PHONE_NUMBER_IS_INVALID)


class TimestampValidator(IValidator):
    def validate(self, value: float):
        length = len(str(int(value)))

        if not (length == 13 or length == 10):
            raise BadRequestException(code=ErrorCodeEnum.INVALID_PASSWORD,
                                      message='Invalid timestamp,'
                                              ' millisecond and seconds based timestamp are supported.')
