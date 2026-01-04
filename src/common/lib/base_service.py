from common.settings import get_settings, Settings, EnvironmentEnum
from util.logger import get_custom_logger, Logger


class BaseService:
    _logger_instance: Logger

    @staticmethod
    def _get_settings() -> Settings:
        return get_settings()

    def is_in_production_mode(self):
        settings = self._get_settings()
        return settings.ENV == EnvironmentEnum.PRODUCTION

    def logger(self) -> Logger:
        if getattr(self, '_logger_instance', None) is None:
            setattr(self, '_logger_instance', get_custom_logger(__name__))
            # self._logger_instance = get_custom_logger(__name__)  # todo, check name is targeting correct file
        return self._logger_instance
