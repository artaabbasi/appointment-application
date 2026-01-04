from typing import Union


class TypeConvertUtil:
    @staticmethod
    def str_to_int(value: str, default=None):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
