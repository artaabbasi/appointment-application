from enum import Enum
from typing import Optional


class RequestLogTypeEnum(str, Enum):
    ASATO = "ASATO"
    HAMMIHAN = "HAMMIHAN"
    SWAGGER = "SWAGGER"
    ERP = "ERP"
    PUBLIC_SITE = "PUBLIC_SITE"
    UNDEFINED = "UNDEFINED"

    @staticmethod
    def get_by_url(url: Optional[str] = None) -> 'RequestLogTypeEnum':
        if url is None:
            return RequestLogTypeEnum.UNDEFINED
        if "api-asato" in url:
            return RequestLogTypeEnum.SWAGGER
        elif "asato" in url:
            return RequestLogTypeEnum.ASATO
        elif "erp" in url:
            return RequestLogTypeEnum.ERP
        elif "hamihan" in url:
            return RequestLogTypeEnum.HAMMIHAN
        elif "mihaninsurance.com" in url:
            return RequestLogTypeEnum.PUBLIC_SITE
        else:
            return RequestLogTypeEnum.UNDEFINED
