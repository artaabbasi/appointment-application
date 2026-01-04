import asyncio
import datetime
from typing import Optional, Callable, Coroutine, Dict, Any

from common.lib.base_service import BaseService
from common.settings import EnvironmentEnum
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)


class BackgroundTaskWrapper(BaseService):
    is_periodic: bool
    frequency_execute_seconds: float
    coroutine_generator: Callable[[], Coroutine]
    dt_last_executed: Optional[datetime.datetime] = None
    task_name: str = ""

    def __init__(self,
                 is_periodic: bool,
                 frequency_execute_seconds: float,
                 coroutine_generator: Callable[[], Coroutine]
                 ) -> None:
        self._latest_task = None
        self.is_periodic = is_periodic
        self.frequency_execute_seconds = frequency_execute_seconds
        self.coroutine_generator = coroutine_generator

    def __post_init__(self):
        if self.task_name is None:
            coro = self.coroutine_generator()
            self.task_name = coro.__qualname__
            coro.close()
        self._latest_task: Optional[asyncio.Task] = None

    def short_info_dict(self) -> Dict[str, Any]:
        info = {
            "is_periodic": self.is_periodic,
            "frequency_execute_seconds": self.frequency_execute_seconds,
            "dt_last_executed": self.dt_last_executed,
            "task_name": self.task_name,
        }
        if self.dt_last_executed is not None:
            info["seconds_since_last_execution"] = (datetime.datetime.now() - self.dt_last_executed).total_seconds()
        return info

    async def start(self):
        logger.info('running task ' + self.task_name, extra={
            "dt_last_executed": self.dt_last_executed,
            "task_name": self.task_name,
        })
        if self.is_periodic is False:
            self._latest_task = asyncio.ensure_future(self.coroutine_generator())
            await self._latest_task
            self.dt_last_executed = datetime.datetime.now()
            return
        if self.frequency_execute_seconds < 0:
            raise Exception(
                f"frequency_execute_seconds is negative: {self.frequency_execute_seconds} for periodic task")
        while True:
            if self.frequency_execute_seconds < 0:
                return
            try:
                self._latest_task = asyncio.ensure_future(self.coroutine_generator())
                await self._latest_task
            except Exception as exc:
                logger.error('error while running task ' + self.task_name, extra={
                    "dt_last_executed": self.dt_last_executed,
                    "task_name": self.task_name,
                    "error": exc
                })
            finally:
                self.dt_last_executed = datetime.datetime.now()
                try:
                    await asyncio.sleep(self.frequency_execute_seconds)
                except Exception as exc:
                    if self._get_settings().ENV != EnvironmentEnum.TEST:
                        raise exc
            pass

    def stop(self):
        self.frequency_execute_seconds = -1000

    def kill(self):
        self.frequency_execute_seconds = -1000
        if self._latest_task is not None:
            self._latest_task.cancel()
