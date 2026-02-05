from typing import Optional, Tuple
import hashlib

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from common.exceptions import UnauthorizedException
from util.logger import get_custom_logger
from module.account.user.enum.user_service_error_code_enum import UserServiceErrorCodeEnum

logger = get_custom_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _normalize_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def verify_password(
    plain_password: str,
    hashed_password: str
) -> Tuple[bool, Optional[str]]:
    try:
        return pwd_context.verify_and_update(
            _normalize_password(plain_password),
            hashed_password
        )
    except UnknownHashError:
        logger.error(
            "UnknownHashError during password verification"
        )
        raise UnauthorizedException(
            "INVALID_CREDENTIALS_PROVIDED"
        )


def get_password_hash(password: str) -> str:
    print(_normalize_password(password))
    return pwd_context.hash(
        _normalize_password(password)
    )
