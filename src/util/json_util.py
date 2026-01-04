import json
from datetime import datetime, date
from json import JSONEncoder
from typing import Dict


from common.exceptions import CustomizedBaseException


class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ValueError):
            return {'_Exception': {'code': obj.args[0]['code'],
                                   'message': obj.args[0]['message'],
                                   'data': obj.args[0]['code']}}
        if isinstance(obj, CustomizedBaseException):
            return {'_Exception': {'code': obj.code,
                                   'message': obj.message,
                                   'data': obj.code}}
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def as_python_object(dct):
    if '_Exception' in dct:
        return CustomizedBaseException(
            dct['_Exception']['code'],
            dct['_Exception']['message'],
            dct['_Exception']['data']
        )
    return dct


class JsonUtil:
    @staticmethod
    def serialize(object_dump: Dict):
        return json.dumps(object_dump, cls=PythonObjectEncoder)

    @staticmethod
    def deserialize(string_json: str):
        return json.loads(string_json, object_hook=as_python_object)

    @staticmethod
    def load_from_file(file_path: str) -> dict:
        with open(file_path, 'r') as f:
            content = f.read()
        return json.loads(content)
