from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from asyncio import current_task

from core.config import settings


class DatabaseHelper:
    """Нужен для подключения к БД"""

    def __init__(self, url: str, echo: bool = False):
        """Создаем движок и фабрику сессий"""
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scope_session(self):
        """ """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """Создаем сессию для подключения к БД во время запросов"""
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        """Создаем сессию для подключения к БД во время запросов"""
        session = self.get_scope_session()
        yield session
        await session.remove()


db_helper = DatabaseHelper(url=settings.url_db, echo=settings.db_echo)
