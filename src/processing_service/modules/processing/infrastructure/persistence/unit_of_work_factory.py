from src.processing_service.config.database import async_session
from .unit_of_work import SQLAlchemyUnitOfWork


async def get_unit_of_work():
    """
    Factory function to create a unit of work.
    For use with FastAPI dependency injection.
    """
    async with async_session() as session:
        async with SQLAlchemyUnitOfWork(session) as uow:
            yield uow