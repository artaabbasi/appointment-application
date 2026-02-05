from sqlalchemy import create_engine
from alembic import context
from database.helpers import get_migration_connection_string

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
from module.account.user.entity.user_entity import UserEntity
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.entity.staff_entity import StaffEntity
from module.account.user.entity.login_activity_entity import LoginActivityEntity

from module.account.authorization.entity.permission_entity import PermissionEntity
from module.account.authorization.entity.role_entity import RoleEntity
from module.account.authorization.entity.role_permission_entity import RolePermissionEntity
from module.account.authorization.entity.user_permission_entity import UserPermissionEntity
from module.account.authorization.entity.user_role_entity import UserRoleEntity

from module.file_manager.bucket.entity.folder_entity import FolderEntity
from module.file_manager.bucket.entity.file_entity import FileEntity
from module.file_manager.bucket.entity.folder_access_entity import FolderAccessEntity
from module.file_manager.bucket.entity.file_meta_data_entity import FileMetaDataEntity

from module.appointment.common.entity.service_entity import ServiceEntity
from module.appointment.common.entity.main_service_entity import MainServiceEntity
from module.appointment.common.entity.operator_entity import OperatorEntity
from module.appointment.common.entity.operator_time_entity import OperatorTimeEntity
from module.appointment.common.entity.category_entity import CategoryEntity
from module.appointment.common.entity.service_category_entity import ServiceCategoryEntity
from module.appointment.common.entity.operator_service_entity import OperatorServiceEntity


from module.appointment.appointment.entity.appointment_entity import AppointmentEntity
from module.appointment.appointment.entity.appointment_item_entity import AppointmentItemEntity
from module.appointment.appointment.entity.cart_entity import CartEntity
from module.appointment.appointment.entity.cart_item_entity import CartItemEntity

from module.logging.request_log.entity.request_log_entity import RequestLogEntity
from module.logging.api_call_log.entity.api_call_log_entity import ApiCallLogEntity


# add your model's MetaData object here
# for 'autogenerate' support
from common.lib.base_entity import BaseEntity

target_metadata = BaseEntity.metadata  # metadata of BASE model which is inherited by entities


# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_migration_connection_string(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_migration_connection_string(),
                                future=True)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
