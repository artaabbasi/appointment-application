from typing import List
from common.lib.base_service import BaseService
from common.config.api_endpoint import ApiEndpoint
from util.request_util import RequestUtil


class SmsUtil(BaseService):
    blacklist_phones: List[str] = []
    async def send_sms(self, recipients_input: List[str], text: str):
        payload = {"recipient": recipients_input, "message": text, "sender": self._get_settings().IP_PANEL_SMS_SENDER}
        url = ApiEndpoint().send_sms_url
        headers = {
            'apikey': self._get_settings().IP_PANEL_API_KEY,
            }
        try:
            response = await RequestUtil.perform_request(method='POST', url=url,
                                                         headers=headers, json=payload,
                                                         timeout=10)
        except Exception as e:
            return f"Error in sending sms : {e}"