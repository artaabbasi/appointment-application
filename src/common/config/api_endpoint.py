from common.lib.base_service import BaseService
from util.request_util import RequestUtil


class ApiEndpoint(BaseService):

    def __init__(self):
        self.ip_panel_gateway = self._get_settings().IP_PANEL_GATEWAY

    @property
    def send_sms_url(self) -> str:
        return RequestUtil.build_url(self.ip_panel_gateway, "sms/send/webservice/single/")
