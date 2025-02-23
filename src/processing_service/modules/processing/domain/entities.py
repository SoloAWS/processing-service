from dataclasses import dataclass, field
from datetime import datetime
import uuid
from ..domain.events import ProcessingStarted, ProcessingCompleted, ProcessingFailed
from ....seedwork.domain.aggregate import AggregateRoot
from .value_objects import ProcessingMetadata, ProcessingResult, ProcessingStatus


@dataclass(kw_only=True)
class ProcessingTask(AggregateRoot):
    metadata: ProcessingMetadata
    raw_data: bytes
    result: ProcessingResult = field(default=None)
    started_at: datetime = field(default=None)
    completed_at: datetime = field(default=None)

    def __init__(
        self,
        metadata: ProcessingMetadata,
        raw_data: bytes,
        result=None,
        started_at=None,
        completed_at=None,
        id=None,
        created_at=None,
        updated_at=None,
    ):
        if id is None:
            id = uuid.uuid4()
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.metadata = metadata
        self.raw_data = raw_data
        self.result = result
        self.started_at = started_at
        self.completed_at = completed_at

    def start_processing(self):
        self.started_at = datetime.now()
        return ProcessingStarted(
            task_id=self.id, metadata=self.metadata, timestamp=datetime.now()
        )

    def complete_processing(self, result: ProcessingResult):
        self.completed_at = datetime.now()
        self.result = result
        return ProcessingCompleted(
            task_id=self.id, result=result, region=self.metadata.region
        )

    def fail_processing(self, error_message: str):
        self.completed_at = datetime.now()
        self.result = ProcessingResult(
            status=ProcessingStatus.FAILED,
            message=error_message,
            region=self.metadata.region,
        )
        return ProcessingFailed(self.id, error_message)
