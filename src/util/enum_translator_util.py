import os
from enum import Enum
from typing import Optional

from common.config.available_languages_enum import AvailableLanguagesEnum
from common.config.translate_library_enum import TranslateLibraryEnum
from common.lib.base_service import BaseService
from util.yaml_util import YamlUtil


class EnumTranslatorUtil(BaseService):
    def __init__(self, lang: AvailableLanguagesEnum, translate_library: TranslateLibraryEnum):
        self.yml_pass = os.path.join(self._get_settings().BASE_DICTIONARY_DIRECTORY,
                                     translate_library.value,
                                     f'{lang.value}.yml')

    def translate(self, enum: Enum) -> Optional[str]:
        return YamlUtil.get_value(self.yml_pass, enum.value)