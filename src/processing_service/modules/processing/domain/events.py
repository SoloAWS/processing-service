from dataclasses import dataclass, field
from datetime import datetime
import uuid
from ....seedwork.domain.events import DomainEvent
from .value_objects import ProcessingMetadata, ProcessingResult


@dataclass
class ProcessingStarted(DomainEvent):
    task_id: uuid.UUID = field(default=None)
    metadata: ProcessingMetadata = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "task_id": str(self.task_id),
            "image_type": self.metadata.image_type.value,
            "region": self.metadata.region,
        }


@dataclass
class ProcessingCompleted(DomainEvent):
    task_id: uuid.UUID = field(default=None)
    result: ProcessingResult = field(default=None)
    region: str = field(default=None)  # NEW FIELD
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "task_id": str(self.task_id),
            "status": self.result.status.value,
            "message": self.result.message,
            "region": self.region,
        }


@dataclass
class ProcessingFailed(DomainEvent):
    task_id: uuid.UUID = field(default=None)
    error_message: str = field(default=None)
    region: str = field(default=None)  # NEW FIELD
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "task_id": str(self.task_id),
            "error_message": self.error_message,
            "region": self.region,
        }
