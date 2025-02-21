from dataclasses import dataclass

from src.processing_service.modules.processing.domain.repositories import (
    ProcessingRepository,
)
from .....seedwork.application.commands import Command, CommandHandler
from ...domain.entities import ProcessingTask
from ...domain.value_objects import ProcessingMetadata, ImageType


@dataclass
class ProcessImageCommand(Command):
    image_type: str
    region: str
    raw_data: bytes
    priority: int = 0


class ProcessImageHandler(CommandHandler):
    def __init__(self, repository: ProcessingRepository):
        self.repository = repository

    async def handle(self, command: ProcessImageCommand):
        metadata = ProcessingMetadata(
            image_type=ImageType[command.image_type],
            region=command.region,
            priority=command.priority,
        )

        task = ProcessingTask(metadata=metadata, raw_data=command.raw_data)

        # Emitir evento de inicio
        start_event = task.start_processing()

        # Guardar tarea
        await self.repository.save(task)

        return task.id
