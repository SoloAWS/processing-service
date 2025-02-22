from typing import List
import uuid
from sqlalchemy import Column, String, LargeBinary, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from ...domain.entities import ProcessingTask
from ...domain.value_objects import (
    ProcessingMetadata,
    ProcessingResult,
    ImageType,
    ProcessingStatus,
)
from datetime import datetime

Base = declarative_base()


class ProcessingTaskDTO(Base):
    __tablename__ = "processing_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=None)
    image_type = Column(SQLEnum(ImageType))
    region = Column(String)
    priority = Column(Integer)
    raw_data = Column(LargeBinary)
    status = Column(SQLEnum(ProcessingStatus))
    message = Column(String)
    created_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)


class SQLProcessingRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_by_id(self, task_id: uuid.UUID) -> ProcessingTask:
        async with self.session_factory() as session:
            dto = await session.get(ProcessingTaskDTO, task_id)
            if not dto:
                return None
            return self._dto_to_entity(dto)

    async def save(self, task: ProcessingTask) -> None:
        dto = self._entity_to_dto(task)
        async with self.session_factory() as session:
            session.add(dto)
            await session.commit()

    async def update(self, task: ProcessingTask) -> None:
        await self.save(task)

    async def get_pending_tasks(self) -> List[ProcessingTask]:
        async with self.session_factory() as session:
            query = (
                await session.query(ProcessingTaskDTO)
                .filter_by(status=ProcessingStatus.PENDING)
                .order_by(ProcessingTaskDTO.priority.desc())
            )
            return [self._dto_to_entity(dto) for dto in query]

    def _dto_to_entity(self, dto: ProcessingTaskDTO) -> ProcessingTask:
        metadata = ProcessingMetadata(
            image_type=dto.image_type, region=dto.region, priority=dto.priority
        )

        result = (
            ProcessingResult(status=dto.status, message=dto.message)
            if dto.status
            else None
        )

        return ProcessingTask(
            id=dto.id,
            metadata=metadata,
            raw_data=dto.raw_data,
            result=result,
            started_at=dto.started_at,
            completed_at=dto.completed_at,
            created_at=dto.created_at,
        )

    def _entity_to_dto(self, entity: ProcessingTask) -> ProcessingTaskDTO:
        dto = ProcessingTaskDTO(
            id=entity.id,
            image_type=entity.metadata.image_type,
            region=entity.metadata.region,
            priority=entity.metadata.priority,
            raw_data=entity.raw_data,
            status=entity.result.status if entity.result else ProcessingStatus.PENDING,
            message=entity.result.message if entity.result else None,
            created_at=entity.created_at,
            started_at=entity.started_at,
            completed_at=entity.completed_at,
        )
        return dto
