import math, random
from typing import Optional

from common.lib.base_service import BaseService


class StringUtilService(BaseService):
    def decompose_birthdate(self, birthdate: str) -> Optional[dict]:
        result = birthdate.split('/')
        if len(result) != 3:
            return None
        return {
            'birth_year': result[0],
            'birth_month': result[1],
            'birth_day': result[2]
        }

    def generate_random_verification_code(self, length: int = 6) -> str:
        # if self.is_in_production_mode:
        #     return '12345'

        digits = "0123456789"
        code = ""

        # length of password can be changed
        # by changing value in range
        for i in range(length):
            code += digits[math.floor(random.random() * 10)]

        return code
