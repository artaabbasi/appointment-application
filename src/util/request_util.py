import json
from typing import Dict, Union, List, Optional
from fastapi import HTTPException

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ContentTypeError, ClientConnectorError, ServerDisconnectedError

from common.exceptions import BadRequestException
from common.lib.main_errors_enum import MainErrorsEnum
from common.util.bale_sender_util import BaleSenderUtil
from util.logger import get_custom_logger
from asyncio import TimeoutError
from json import loads, dumps
logger = get_custom_logger(__name__)


class ResponseDetail:
    def __init__(self,
                 body: Union[Dict, List],
                 payload: Union[Dict, List],
                 headers: Union[Dict, List, any],
                 req_headers: Union[Dict, List, any],
                 status_code: int,
                 url: Optional[str] = None):
        self.body = body
        self.payload = payload
        self.headers = headers
        self.req_headers = req_headers
        self.status_code = status_code
        self.url = url

    def was_okay(self) -> bool:
        return str(self.status_code).startswith('2')

    async def raise_error_if_response_was_not_okay(self):
        if not self.was_okay():
            body = getattr(self, 'body', {})
            if body is None:
                body = {}
            detail = body.get('detail', body)
            message = f"""❌  LOOK an error in external apis!  ❌
            
⚠️  url: 
```
{self.url}
```
⚠️  status code: 
```
{self.status_code}
```
⚠️  headers: 
```
{json.dumps(self.req_headers, indent=2, ensure_ascii=False) if isinstance(self.req_headers, dict) else self.req_headers}
```
⚠️  payload: 
```
{json.dumps(self.payload, indent=2, ensure_ascii=False) if isinstance(self.payload, dict) else self.payload}
```
⚠️  detail: 
```
{json.dumps(detail, indent=2, ensure_ascii=False) if isinstance(detail, dict) else detail}
```
"""

            await BaleSenderUtil().send_log_message(message)

            raise HTTPException(status_code=422,
                                detail=detail,
                                headers={"Response-Status-Code": str(self.status_code)})

    def __repr__(self):
        return f'ResponseDetail(status_code={self.status_code},' \
               f'headers={self.headers},' \
               f'body={self.body})'


class RequestUtil:
    @staticmethod
    async def _handle_request(session: ClientSession,
                              method: str,
                              url: str,
                              *,
                              headers: Dict = None,
                              params: Dict = None,
                              data: Dict = None,
                              json: Dict = None) -> ResponseDetail:
        try:
            req_kwargs = {}
            if headers is not None:
                req_kwargs['headers'] = headers
            if params is not None:
                req_kwargs['params'] = params
            if json is not None:
                req_kwargs['json'] = json
            if data is not None:
                req_kwargs['data'] = data
            async with session.request(method, url, **req_kwargs, verify_ssl=False) as response:
                try:
                    logger.info('response from calling: ', extra={
                        'response_data': await response.json(), 'response': response, 'url': url,
                        'headers': headers, 'params': params, 'json': json, 'data': data, 'status_code': response.status
                    })
                    content = await response.json()
                except Exception as e:
                    try:
                        text = await response.text()
                        content = loads(text)
                        logger.info('response from calling: ', extra={
                            'response_data': content, 'response': response, 'url': url,
                            'headers': headers, 'params': params, 'json': json, 'data': data, 'status_code': response.status
                        })
                        text = await response.text()
                        content = loads(text)
                    except Exception as e:
                        logger.info('non json response from calling: ', extra={
                            'response': await response.read(), 'url': url,
                            'headers': headers, 'params': params, 'json': json, 'data': data, 'status_code': response.status
                        })
                        content = await response.read()
                        if response.status != 204 and response.status != 200:
                            logger.exception(e)
                            logger.error(f"Wrong ContentType request returned non-json response.")
                            logger.error(f"response was {content}")
                            raise HTTPException(status_code=422, detail=content,
                                headers={"Response-Status-Code": str(response.status)})

        except TimeoutError as e:
            logger.exception(e)
            logger.error(f"Request timed out.")
            logger.error(f"request url was {url}")
            raise HTTPException(status_code=422, detail='Request timed out',
                                headers={"Response-Status-Code": "500"})
        except ClientConnectorError as e:
            logger.exception(e)
            logger.error(f"Request connection failed.")
            logger.error(f"request url was {url}")
            raise HTTPException(status_code=422, detail='Request connection failed',
                                headers={"Response-Status-Code": "500"})
        except ServerDisconnectedError as e:
            logger.exception(e)
            logger.error(f"Server disconnected.")
            logger.error(f"request url was {url}")
            raise HTTPException(status_code=422, detail='Server disconnected',
                                headers={"Response-Status-Code": "500"})
        except Exception as e:
            logger.exception(e)
            logger.error(f"Unexpected error.")
            logger.error(f"request url was {url}")
            raise HTTPException(status_code=422, detail='Unexpected error',
                                headers={"Response-Status-Code": "500"})
        res = ResponseDetail(content, json, response.headers, headers, response.status, url)

        logger.debug('Request-response log.',
                     extra={'url': url,
                            'request': {'query params': params,
                                        'body': json},
                            'Response': {
                                'status code': res.status_code,
                                'body': res.body,
                            }},
                     )
        return res

    @staticmethod
    async def perform_request(
            method: str,
            url: str,
            *,
            headers: Dict = None,
            params: Dict = None,
            json: Dict = None,
            data: Dict = None,
            timeout: int = 300) -> ResponseDetail:
        assert method in ['POST', 'GET', 'PUT', 'DELETE', 'PATCH'], 'Invalid http method for request.'
        timeout = ClientTimeout(total=timeout) if timeout else ClientTimeout(total=300)
        async with ClientSession(timeout=timeout) as session:
            return await RequestUtil._handle_request(session,
                                                     method,
                                                     url,
                                                     headers=headers,
                                                     params=params,
                                                     json=json,
                                                     data=data,
                                                     )

    @staticmethod
    def build_url(base_url: str, *url_parts: Union[List[str], str]) -> str:
        return '/'.join([base_url, *url_parts])
