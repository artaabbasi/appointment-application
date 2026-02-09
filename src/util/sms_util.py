from typing import List
from aiohttp import ClientTimeout, ClientSession
from common.lib.base_service import BaseService
from requests.auth import HTTPBasicAuth
from requests import Session
from common.config import ApiEndpoint


class SmsUtil(BaseService):
    blacklist_phones: List[str] = []
    async def send_sms(self, recipients_input: List[str], text: str):
        payload = {"recipient": recipients_input, "message": text, "sender": self._get_settings().IP_PANEL_SMS_SENDER}
        url = ApiEndpoint().send_sms_url
        timeout = ClientTimeout(total=1)
        headers = {
            'apikey': self._get_settings().IP_PANEL_API_KEY,
            }
        try:
            async with ClientSession(timeout=timeout) as session:
                async with session.request('POST', url, json=payload, verify_ssl=False, headers=headers) as response:
                    pass
        except Exception as e:
            return f"Error in sending sms : {e}"
