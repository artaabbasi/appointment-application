import re

from fastapi import Request, HTTPException
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from common.config.http_method_enum import HTTPMethodEnum
from common.logging.enum.request_log_type_enum import RequestLogTypeEnum
from common.logging.schema.request_log_in_schema import RequestLogInSchema
from module.logging.request_log.service.request_log_service import RequestLogService


class RequestLoggerMiddleware(BaseHTTPMiddleware):

    EXCLUDE_PATTERNS = [r"/metrics",
                        r"/logs/request-log"]  # regex patterns

    def _is_excluded(self, url: str) -> bool:
        return any(re.match(pattern, url) for pattern in self.EXCLUDE_PATTERNS)

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        start_time = time.time()
        async def receive() -> Message:
            return {"type": "http.request", "body": body, "more_body": False}

        request = Request(request.scope, receive)

        url = str(request.url)
        referer = request.headers.get("referer")

        if self._is_excluded(url):
            return await call_next(request)

        log_type = RequestLogTypeEnum.get_by_url(referer)
        request_log = await RequestLogService().create_request_log(
            RequestLogInSchema(
                type=log_type,
                url=url,
                client=referer,
                method=HTTPMethodEnum.get_enum_from_str(request.method),
                request_headers=str(request.headers),
                request_payload=str(body)
            )
        )

        try:
            response = await call_next(request)

        except Exception as e:
            process_time = time.time() - start_time
            status_code = 500
            body =  str(e)
            headers = None
            if isinstance(e, HTTPException):
                status_code = e.status_code
                body = e.detail
            await RequestLogService().update_request_log(
                request_log.id,
                RequestLogInSchema(
                    process_time=process_time,
                    response_status_code=status_code,
                    response_body=body,
                    response_headers=headers
                )
            )
            raise

        process_time = time.time() - start_time
        try:
            response_body = str(response.body)
        except AttributeError:
            response_body = None
        await RequestLogService().update_request_log(
            request_log.id,
            RequestLogInSchema(
                process_time=process_time,
                response_status_code=response.status_code,
                response_body=response_body,
                response_headers=str(response.headers)
            )
        )
        return response
