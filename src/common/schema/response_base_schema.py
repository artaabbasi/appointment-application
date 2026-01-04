from typing import Generic, TypeVar, List, Optional

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseGenericResponse(BaseModel, Generic[T]):
    status: str = 'ok'


class GenericResponseSingleSchema(BaseGenericResponse, Generic[T]):
    data: Optional[T]

    @staticmethod
    def return_response(data: Optional[T] = None):
        return {'status': 'ok',
                'data': data}


class GenericResponseListSchema(BaseGenericResponse, Generic[T]):
    data: List[T]
    page: Optional[int] = None
    size: Optional[int] = None
    count: Optional[int] = None

    @staticmethod
    def return_response(data: List[T], page: int = None, size: int = None, count: int = None):
        return {'status': 'ok',
                'data': data, 'page': page, 'size': size, 'count': count}
