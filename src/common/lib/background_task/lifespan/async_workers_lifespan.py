import asyncio
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_lifespan_manager import State

from common.lib.background_task.background_task_wrapper import BackgroundTaskWrapper
from common.lib.background_task.lifespan.lifespan_tasks import get_tasks
from database.run_migrations import run_migrations
from module.account.user.service import AdminAuthService
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)

state = {'routines': []}


async def lifespan_add_task(task: BackgroundTaskWrapper):
    state['routines'].append(asyncio.ensure_future(task.start()))


async def service_workers_lifespan(app: FastAPI) -> AsyncIterator[State]:
    logger.info('running module worker tasks')
    run_migrations()
    await AdminAuthService().create_default_admin_user()
    tasks = await get_tasks()
    for task in tasks:
        state['routines'].append(asyncio.ensure_future(task.start()))
    yield state
    for task in tasks:
        task.kill()
    state.clear()
    logger.info('tearing down module worker tasks...')
