from typing import Dict, Type, List, Union
from fastapi import HTTPException


def generate_openapi_response_dictionary_schema(status_code: int,
                                                description: str,
                                                example_dict: Dict,
                                                application_type: str = 'application/json') -> Dict:
    """
    Generates a dictionary formatted as bellow, the result dict can be used as openapi response schema for
    swagger documentation.

    {
       "401":{
          "description":"Wrong format for cloud subsystem token.",
          "content":{
             "application/json":{
                "example":{
                   "detail":"Wrong format for cloud token: `your token`."
                }
             }
          }
       }
    }
    """
    result = dict()
    result[status_code] = {}
    result[status_code]['description'] = description
    result[status_code]['content'] = {}
    result[status_code]['content'][application_type] = {}
    result[status_code]['content'][application_type]['example'] = example_dict
    return result


def generate_schema_from_exceptions(exceptions: Union[List[Type[HTTPException]], Type[HTTPException]],
                                    description: str,
                                    exceptions_kwargs: Dict = None,
                                    ) -> Dict:
    """
    Generates openapi error schema from exceptions.

    :param exceptions: List of exception, also it can be a single exception.
    :param description: Description which will be placed in the openapi.
    :param exceptions_kwargs: A dictionary of possible exception arguments which will be passed to the exception itself.
                                example : exceptions_kwargs = {
                                                    SSHKeyNotFound: { "_id" : 34,}
                                                    }
                                by this an instance of SSHKeyNotFound will be created for documentation with that input.
                                As:  SSHKeyNotFound(**exception_kwargs.get(SSHKeyNotFound))

    :return: A dictionary which can be used in fastapi routers to add openapi documentation.
    """
    if not exceptions_kwargs:
        exceptions_kwargs = {}
    if not isinstance(exceptions, List):
        exceptions = [exceptions, ]
    instances = [exception(**exceptions_kwargs.get(exception, {})) for exception in exceptions]
    status_codes = {instance.status_code for instance in instances}
    assert len(status_codes) == 1, "Exceptions with different status codes can not be documented to-gather."
    detail = ' or '.join([instance.detail for instance in instances])
    return generate_openapi_response_dictionary_schema(status_code=instances[0].status_code,
                                                       example_dict={'detail': detail},
                                                       description=description)
