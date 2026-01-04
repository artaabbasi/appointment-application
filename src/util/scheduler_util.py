import asyncio
from datetime import datetime

from common.lib.base_service import BaseService
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)


class SchedulerUtil(BaseService):
    async def scheduler(self, weekdays: list[int],
                        start_hour: int,
                        end_hour: int,
                        scheduled_task: any,
                        *args):
        current_time = datetime.now()
        logger.info(f"Trying to run {scheduled_task} with {args}, weekday: {current_time.weekday()}, task weekday: {weekdays}; "
                           f"now: {current_time.hour}, task start_hour: {start_hour} and task end_hour: {end_hour}; "
                           f"condition: {current_time.weekday() in weekdays and start_hour <= current_time.hour < end_hour};")
        if current_time.weekday() in weekdays and start_hour <= current_time.hour < end_hour:
            try:
                await scheduled_task(*args)
            except Exception as e:
                logger.error(f"Trying to run {scheduled_task} failed, Exception: {e}")