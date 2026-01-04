from contextlib import asynccontextmanager

from sqlalchemy.orm import with_loader_criteria, sessionmaker, declarative_base
from sqlalchemy import Column, DateTime, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from database.helpers import get_database_connection_string


RECYCLE_POOL_IN = 7.5 * 60 * 60
engine = create_async_engine(get_database_connection_string(),
                                future=True,
                                pool_recycle=RECYCLE_POOL_IN,
                                pool_size=10,
                                max_overflow=20,
                                pool_timeout=30,
                                pool_pre_ping=True
                             )

AsyncSessionLocal = sessionmaker(bind=engine,
                                 expire_on_commit=False,
                                 class_=AsyncSession,)
ses = AsyncSessionLocal()
Base = declarative_base()


def add_listener_for_session(session):
    @event.listens_for(session.sync_session, "do_orm_execute")
    def _add_filtering_criteria(execute_state):
        """Intercept all ORM queries.   Add a with_loader_criteria option to all
        of them.

        This option applies to SELECT queries and adds a global WHERE criteria
        (or as appropriate ON CLAUSE criteria for join targets)
        to all objects of a certain class or superclass.

        """
        if (
            not execute_state.is_column_load
            and not execute_state.is_relationship_load
            and not execute_state.execution_options.get("include_deleted", False)
        ):
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    HasSoftDelete,
                    lambda cls: cls.deleted_at.is_(None),
                    include_aliases=True,
                )
            )


class HasSoftDelete:
    deleted_at = Column(DateTime)


class Dictable:
    def to_dict(self):
        class_vars = vars(self.__class__)  # get any "default" attrs defined at the class level
        inst_vars = vars(self)  # get any attrs defined on the instance (self)
        all_vars = dict(class_vars)
        all_vars.update(inst_vars)
        # filter out private attributes
        public_vars = {k: v for k, v in all_vars.items() if not k.startswith('_')}
        return public_vars


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        add_listener_for_session(session)
        yield session
