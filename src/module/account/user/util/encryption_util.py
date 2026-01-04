from typing import Dict, Union
import json
from cryptography.fernet import Fernet, InvalidToken

from common.exceptions import (
    UnauthorizedException
)
from module.user.enum.error_code_enum import ErrorCodeEnum
from common.settings import get_settings
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)

settings = get_settings()
TOKEN_EXPIRATION_IN_SECONDS = 48 * 60 * 60


def convert_dict_to_bytes(data: Dict) -> bytes:
    return json.dumps(data).encode('utf-8')


def convert_bytes_to_dict(data: bytes) -> Dict:
    return json.loads(data.decode('utf-8'))


def encrypt_data(data: Dict) -> str:
    """
    This utility function gets a dictionary and returns an url friendly encrypted
    string based on the data
    """
    bytes_data = convert_dict_to_bytes(data)
    f = Fernet(settings.SECRET_KEY)
    encrypted_bytes = f.encrypt(bytes_data)
    result_string = encrypted_bytes.decode('utf-8')
    return result_string


def _decrypt(f: Fernet, bytes: bytes, ignore_expiration: bool = False):
    if ignore_expiration:
        try:
            result = f.decrypt(bytes)
            result_dict = convert_bytes_to_dict(result)
            raise UnauthorizedException(code=ErrorCodeEnum.EXPIRED_VERIFICATION_CODE_PROVIDED,
                                        message=result_dict.get('email'))
        except InvalidToken:
            raise UnauthorizedException(code=ErrorCodeEnum.INVALID_VERIFICATION_CODE_PROVIDED)

    else:
        result = f.decrypt(bytes, TOKEN_EXPIRATION_IN_SECONDS)
        return result


def decrypt_data(data: str) -> Union[Dict, bool]:
    """
    This utility function get an encrypted string and returns a
    decrypted dict from the data
    """
    bytes_data = data.encode('utf-8')
    f = Fernet(settings.SECRET_KEY)
    try:
        result_bytes = _decrypt(f, bytes_data)
    except InvalidToken:
        result_bytes = _decrypt(f, bytes_data, ignore_expiration=True)
    return convert_bytes_to_dict(result_bytes)
