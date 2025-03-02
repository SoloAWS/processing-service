from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from src.processing_service.seedwork.application.unit_of_work import UnitOfWork
from .repositories import SQLProcessingRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.processing_repository = None

    async def __aenter__(self):
        self.processing_repository = SQLProcessingRepository(self._session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    @asynccontextmanager
    async def transaction(self):
        try:
            yield
            await self.commit()
        except Exception as e:
            await self.rollback()
            raise e