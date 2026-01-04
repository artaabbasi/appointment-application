from typing import Any
import requests
from zeep import Client, Transport, exceptions
from zeep.helpers import serialize_object
from zeep.xsd.valueobjects import CompoundValue
from zeep.xsd.schema import Schema
from lxml import etree

from common.exceptions import BadRequestException
from common.lib.base_service import BaseService
from common.lib.main_errors_enum import MainErrorsEnum
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)


class SoapUtil(BaseService):
    def __init__(self, wsdl_url: str):
        self.wsdl_url = wsdl_url

    async def _get_client(self, timeout: int = 300) -> Client:
        session = requests.Session()
        session.verify = False
        transport = Transport(session=session, timeout=timeout)
        try:
            client = Client(self.wsdl_url, transport=transport)
            return client
        except Exception as e:
            raise BadRequestException(MainErrorsEnum.EXTERNAl_API_NOT_WORKING)


    def _serialize_zeep_object(self, obj: Any):
        if isinstance(obj, dict):
            return {key: self._serialize_zeep_object(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_zeep_object(item) for item in obj]
        elif isinstance(obj, CompoundValue):
            return serialize_object(obj)
        elif isinstance(obj, etree._Element):
            return etree.tostring(obj, encoding="unicode")
        elif isinstance(obj, Schema):
            return str(obj)

        return obj

    async def call_soap_service(self, method_name: str, timeout: int = 300, **kwargs) -> dict:
        client = await self._get_client(timeout)
        try:
            response = getattr(client.service, method_name)(**kwargs)
            logger.info('response from calling: ', extra={
                'response_data': response, 'url': self.wsdl_url,
                'method name': method_name, 'params': kwargs})
            serialized_data = self._serialize_zeep_object(serialize_object(response))
            return {
                "success": True,
                "data": serialized_data
            }
        except exceptions.Fault as fault:
            logger.error('fault from api call from calling: ', extra={
                'exception': fault, 'url': self.wsdl_url,
                'method name': method_name, 'params': kwargs})
            return {"success": False, "detail": f"SOAP Fault: {fault.message}"}
        except exceptions.TransportError as transport_err:
            logger.error('transport_err from api call from calling: ', extra={
                'exception': transport_err, 'url': self.wsdl_url,
                'method name': method_name, 'params': kwargs})
            return {"success": False, "detail": f"Transport Error: {transport_err}"}
        except exceptions.XMLSyntaxError as xml_err:
            logger.error('xml_err from api call from calling: ', extra={
                'exception': xml_err, 'url': self.wsdl_url,
                'method name': method_name, 'params': kwargs})
            return {"success": False, "detail": f"XML Syntax Error: {xml_err}"}
        except exceptions.Error as general_err:
            logger.error('general_err from api call from calling: ', extra={
                'exception': general_err, 'url': self.wsdl_url,
                'method name': method_name, 'params': kwargs})
            return {"success": False, "detail": f"Zeep Error: {general_err}"}
        except Exception as e:
            logger.error('exception from api call from calling: ', extra={
                'exception': e, 'url': self.wsdl_url,
                'method name': method_name, 'params': kwargs})
            return {"success": False, "detail": f"Unexpected Error: {e}"}