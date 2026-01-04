from module.account.user.service.admin_auth_service import AdminAuthService
import asyncio


def create_default_admin_user():
    asyncio.run(AdminAuthService().create_default_admin_user())
