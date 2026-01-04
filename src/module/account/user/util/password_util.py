from typing import Optional, Tuple
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from common.exceptions import UnauthorizedException
from util.logger import get_custom_logger
from module.account.user.enum.user_service_error_code_enum import UserServiceErrorCodeEnum

logger = get_custom_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> Tuple[bool, Optional[str]]:
    try:
        return pwd_context.verify_and_update(plain_password, hashed_password)
    except UnknownHashError as err:
        logger.error('UnknownHashError error, plain_password: %s, hashed_password: %s', plain_password, hashed_password)
        raise UnauthorizedException('INVALID_CREDENTIALS_PROVIDED')


def get_password_hash(password):
    return pwd_context.hash(password)
