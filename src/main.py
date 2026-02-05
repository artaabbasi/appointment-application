from fastapi import FastAPI
from common.settings import get_settings, EnvironmentEnum
from middleware import RequestLoggerMiddleware

from util.logger import get_custom_logger
from common.lib.background_task.lifespan.lifespan_manager import manager
from fastapi.middleware.cors import CORSMiddleware

from module.gateway.account.controller.auth_controller import router as auth_router
from module.gateway.account.controller.admin_auth_controller import router as admin_auth_router
from module.gateway.account.controller.customer_controller import router as customer_router
from module.gateway.account.controller.admin_controller import router as admin_router
from module.gateway.account.controller.permission_controller import router as permission_router
from module.gateway.account.controller.role_controller import router as role_router
from module.gateway.file_manager.controller.bucket_controller import router as bucket_router
from module.gateway.logging.controller.log_controller import router as log_router
from module.gateway.appointment.controller.common_controller import router as appointment_common_router
from module.gateway.appointment.controller.appointment_controller import router as appointment_router
from module.gateway.appointment.controller.cart_controller import router as appointment_cart_router

settings = get_settings()

enable_debug_mode = not (settings.ENV == EnvironmentEnum.PRODUCTION)

app = FastAPI(title="Backend API",
              description='monolithic modular backend!',
              debug=enable_debug_mode,
              lifespan=manager
              )

origins = settings.CORS_ALLOW_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_custom_logger(__name__)

app.add_middleware(RequestLoggerMiddleware)

app.include_router(auth_router)
app.include_router(admin_auth_router)
app.include_router(customer_router)
app.include_router(admin_router)
# app.include_router(permission_router)
# app.include_router(role_router)
app.include_router(bucket_router)
app.include_router(log_router)
app.include_router(appointment_common_router)
app.include_router(appointment_router)
app.include_router(appointment_cart_router)

# @app.on_event("startup")
# async def startup_event():
#     run_migrations()
#     run_managers()
