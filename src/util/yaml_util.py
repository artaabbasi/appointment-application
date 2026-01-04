from typing import Optional, Union

import yaml


class YamlUtil:
    @staticmethod
    def get_data(path: str):
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data

    @staticmethod
    def get_value(path: str, key: str) -> Union[str, list]:
        data = YamlUtil.get_data(path)
        return data.get(key, None)
