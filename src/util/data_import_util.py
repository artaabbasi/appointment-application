import re
from typing import Optional, List, Union


class DataImportUtil:

    @staticmethod
    async def get_raw_string(input_value: any) -> Optional[str]:
        if isinstance(input_value, float):
            return None
        return str(input_value)

    @staticmethod
    async def get_raw_int(input_value: any) -> Optional[int]:
        try:
            return int(input_value)
        except ValueError:
            return None

    @staticmethod
    async def get_raw_float(input_value: any) -> Optional[float]:
        try:
            return float(input_value)
        except ValueError:
            return None

    @staticmethod
    async def fa_string_bool(input_value: str) -> bool:
        return input_value in ["بله", "دارد"]


    @staticmethod
    async def extract_decimal_numbers(input_string: Union[str, int, None]) -> Optional[List[int]]:
        if isinstance(input_string, str):
            decimal_numbers = re.findall(r'\d+\.\d+|\d+', input_string)
            return [int(decimal) for decimal in decimal_numbers]
        elif isinstance(input_string, int):
            return [int(input_string)]
        return None
