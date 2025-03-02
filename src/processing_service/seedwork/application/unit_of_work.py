from abc import ABC, abstractmethod
from contextlib import asynccontextmanager


class UnitOfWork(ABC):
    @abstractmethod
    async def commit(self):
        """Commit the current transaction"""
        pass

    @abstractmethod
    async def rollback(self):
        """Rollback the current transaction"""
        pass

    @abstractmethod
    @asynccontextmanager
    async def transaction(self):
        """Context manager for transactions"""
        try:
            yield
            await self.commit()
        except Exception as e:
            await self.rollback()
            raise e