import os
from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command

# All the database models must be imported here.
from common.lib.base_entity import BaseEntity
# Only in this case they will be created in migrations.

from common.settings import EnvironmentEnum

from database.helpers import get_migration_connection_string
from util.logger import get_custom_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
logger = get_custom_logger(__name__)

if os.environ.get('ENV') == EnvironmentEnum.TEST:
    db_name = os.environ.get('TEST_DATABASE_NAME')
else:
    db_name = os.environ.get('DATABASE_NAME')


def check_if_database_is_empty():
    engine = create_engine(get_migration_connection_string(), future=True, echo=True)
    with engine.connect() as conn:
        result = conn.execute(text(f" SELECT  count(distinct table_name) c  FROM information_schema.tables"
                                   f" WHERE table_catalog='{db_name}' and table_schema='public';"))
        result = result.fetchone()
        return result[0] == 0


def stamp_alembic_head():
    alembic_cfg = Config(os.path.join(current_dir, '../alembic.ini'))
    alembic_cfg.set_main_option('script_location',
                                os.path.join(current_dir, 'migrations'))
    command.stamp(alembic_cfg, "head")


def init_tables():
    engine = create_engine(get_migration_connection_string(), future=True, echo=True)
    BaseEntity.metadata.create_all(engine)
    stamp_alembic_head()


def upgrade_head():
    alembic_cfg = Config(os.path.join(current_dir, '../alembic.ini'))
    alembic_cfg.set_main_option('script_location',
                                os.path.join(current_dir, 'migrations'))
    command.upgrade(alembic_cfg, 'head')


def run_migrations():
    logger.info("Caution: This will try to create tables on a raw database.")
    logger.info("This database will create all tables in raw database and stamps alembic revision to HEAD.")
    if not check_if_database_is_empty():
        logger.info("Database was not empty. So run the latest migrations... ")
    else:
        logger.info("Database was empty.")
        init_tables()
    logger.info("Running migrations ...")
    upgrade_head()
    logger.info("Running migrations Finished.")


if __name__ == '__main__':
    run_migrations()
