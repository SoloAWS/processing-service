from dataclasses import dataclass
from enum import Enum
from ....seedwork.domain.value_objects import ValueObject


class ImageType(Enum):
    XRAY = "XRAY"
    MRI = "MRI"
    HISTOLOGY = "HISTOLOGY"
    ULTRASOUND = "ULTRASOUND"
    MAMMOGRAPHY = "MAMMOGRAPHY"


class ProcessingStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ProcessingMetadata(ValueObject):
    image_type: ImageType
    region: str
    priority: int = 0


@dataclass(frozen=True)
class ProcessingResult(ValueObject):
    status: ProcessingStatus
    message: str
    processed_data: dict = None
