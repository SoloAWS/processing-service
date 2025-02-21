from abc import ABC, abstractmethod
from typing import List
import uuid
from .entities import ProcessingTask


class ProcessingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, task_id: uuid.UUID) -> ProcessingTask:
        """Get a processing task by ID"""
        pass

    @abstractmethod
    async def save(self, task: ProcessingTask) -> None:
        """Save a processing task"""
        pass

    @abstractmethod
    async def update(self, task: ProcessingTask) -> None:
        """Update a processing task"""
        pass

    @abstractmethod
    async def get_pending_tasks(self) -> List[ProcessingTask]:
        """Get all pending processing tasks"""
        pass
