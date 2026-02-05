import traceback

from fastapi import Request, HTTPException, status
from typing import Dict, Optional

from common.config.available_languages_enum import AvailableLanguagesEnum
from common.config.translate_library_enum import TranslateLibraryEnum
from util.enum_translator_util import EnumTranslatorUtil
from util.logger import get_custom_logger
import asyncio

logger = get_custom_logger(__name__)


translator = EnumTranslatorUtil(AvailableLanguagesEnum.FARSI, TranslateLibraryEnum.ERROR)


class CustomHttpException(HTTPException):
    detail: Dict

    def __init__(self, status_code, detail: Dict, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.detail = detail
        try:
            message = translator.translate(self.detail.get("code"))
        except Exception:
            message = ""
        self.detail.update({"message": message})


class ForbiddenException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail={'code': code, 'message': message}, headers=headers)


class BadRequestException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail={'code': code, 'message': message}, headers=headers)


class NotFoundException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail={'code': code, 'message': message}, headers=headers)


class InternalServerErrorException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'code': code, 'message': message}, headers=headers)


class UnauthorizedException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail={'code': code, 'message': message}, headers=headers)


class PreConditionFailedException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_412_PRECONDITION_FAILED, detail={'code': code, 'message': message}, headers=headers)


class ConflictException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail={'code': code, 'message': message}, headers=headers)


class UnProcessableEntityException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'code': code, 'message': message}, headers=headers)


class PaymentRequiredException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail={'code': code, 'message': message}, headers=headers)


class NotImplementedException(CustomHttpException):
    def __init__(self, code, message=None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail={'code': code, 'message': message}, headers=headers)


class CustomizedBaseException(Exception):
    data: Dict
    message: str
    code: int

    def __init__(self, code, message, data):
        super().__init__()
        self.code = code
        self.message = message
        self.data = data
