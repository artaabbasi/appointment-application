from typing import Dict, Union
import logging
import os
from pythonjsonlogger import jsonlogger

from util.timestamp import DatetimeUtil
from common.settings import get_settings, EnvironmentEnum

settings = get_settings()


class Logger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict, record: logging.LogRecord, message_dict: Dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if not log_record.get('timestamp'):
            now = DatetimeUtil.utc_now_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        log_record['level'] = record.levelname
        log_record['appname'] = settings.PROJECT_NAME
        if record.levelname.lower() != "notice":
            log_record["line_num"] = record.lineno
            log_record["file_name"] = record.filename
            log_record["func_name"] = record.funcName


def get_custom_logger(logger_name: str) -> Logger:
    logging.setLoggerClass(Logger)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = CustomJsonFormatter(json_ensure_ascii=False)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_directory = os.path.join(current_dir, '..', 'logs')
    if not os.path.exists(logs_directory):
        os.mkdir(logs_directory)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    fh_error = logging.FileHandler(os.path.join(logs_directory, 'errors.log'))
    fh_error.setLevel(logging.ERROR)
    fh_error.setFormatter(formatter)
    logger.addHandler(fh_error)

    fh_debug = logging.FileHandler(os.path.join(logs_directory, 'combined.log'))
    fh_debug.setLevel(logging.INFO)
    fh_debug.setFormatter(formatter)
    logger.addHandler(fh_debug)
    return logger
