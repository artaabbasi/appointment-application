from common.settings import get_settings, EnvironmentEnum


async def get_tasks():
    settings = get_settings()
    if settings.ENV == EnvironmentEnum.BG_TASK:
        return []

    tasks = [
    ]
    return tasks