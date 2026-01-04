from typing import List

from common.lib.base_service import BaseService
from requests.auth import HTTPBasicAuth
from requests import Session


class SmsUtil(BaseService):
    blacklist_phones: List[str] = []
    async def send_sms(self, recipients_input: List[str], text: str):
        pass
