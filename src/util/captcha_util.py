import base64
import random
import string
from typing import Tuple
from datetime import datetime
from captcha.image import ImageCaptcha

from database.redis_setup import get_redis_session
from util.redis_util import RedisUtil


class CaptchaUtil:

    @staticmethod
    def code_generator(size: int):
        return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))

    async def generate_captcha(self) -> Tuple[bytes, str]:
        captcha: str = self.code_generator(6)
        image = ImageCaptcha()
        image.character_rotate = (-5, 5)
        image.character_offset_dx = (0, 2)
        image.character_offset_dy = (0, 4)
        image.character_warp_dx = (0.05, 0.1)
        image.character_warp_dy = (0.1, 0.2)
        image.word_space_probability = 0.7
        image.word_offset_dx = 0.1
        data = image.generate(captcha)
        data = base64.b64encode(data.getvalue())
        await RedisUtil().set_key(f'captcha:{datetime.now().timestamp()}', captcha.lower(), 120)
        return data, captcha

    async def verify_captcha(self, input_captcha: str) -> bool:
        pattern = "captcha:*"

        cursor = 0
        async with get_redis_session() as r:
            while True:
                cursor, captcha_keys = await r.scan(cursor=cursor, match=pattern, count=100)

                for captcha_key in captcha_keys:
                    stored_captcha = (await r.get(captcha_key)).decode('utf-8')

                    if stored_captcha == input_captcha.lower():
                        await r.delete(captcha_key)
                        return True

                if cursor == 0:
                    break

        return False
