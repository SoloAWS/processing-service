from fastapi import FastAPI, Form, HTTPException, UploadFile, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from ....config.settings import Settings
from ..application.commands.process_image import (
    ProcessImageCommand,
    ProcessImageHandler,
)
from ..application.queries.get_task_status import (
    GetTaskStatusQuery,
    GetTaskStatusHandler,
)
from ..domain.value_objects import ImageType
from ....config.database import get_session
from ..infrastructure.persistence.repositories import SQLProcessingRepository
from ..application.events.event_handlers import PulsarEventHandler

app = FastAPI(title="Processing Service")

settings = Settings()


class ProcessImageRequest(BaseModel):
    image_type: str
    region: str
    priority: Optional[int] = 0


class ProcessingResponse(BaseModel):
    task_id: str
    message: str = "Processing started"


class TaskStatusResponse(BaseModel):
    id: str
    status: str
    message: str
    started_at: Optional[str]
    completed_at: Optional[str]


async def get_command_handler(
    session: AsyncSession = Depends(get_session),
) -> ProcessImageHandler:
    settings = Settings()
    repository = SQLProcessingRepository(lambda: session)
    # Initialize PulsarEventHandler without host parameter
    event_handler = PulsarEventHandler()
    return ProcessImageHandler(repository=repository, event_handler=event_handler)


async def get_query_handler(
    session: AsyncSession = Depends(get_session),
) -> GetTaskStatusHandler:
    repository = SQLProcessingRepository(lambda: session)
    return GetTaskStatusHandler(repository=repository)


@app.post("/process", response_model=ProcessingResponse)
async def process_image(
    image_type: str = Form(...),
    region: str = Form(...),
    priority: Optional[int] = Form(0),
    file: UploadFile = Form(...),
    command_handler: ProcessImageHandler = Depends(get_command_handler),
):
    try:
        if image_type not in ImageType.__members__:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image type. Must be one of: {list(ImageType.__members__.keys())}",
            )

        content = await file.read()

        command = ProcessImageCommand(
            image_type=image_type,
            region=region,
            raw_data=content,
            priority=priority,
        )

        task_id = await command_handler.handle(command)
        return ProcessingResponse(task_id=str(task_id))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str, query_handler: GetTaskStatusHandler = Depends(get_query_handler)
):
    try:
        task_uuid = uuid.UUID(task_id)
        query = GetTaskStatusQuery(task_id=task_uuid)
        result = await query_handler.handle(query)

        if not result.result:
            raise HTTPException(
                status_code=404, detail=f"Task with id {task_id} not found"
            )

        return result.result

    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid task ID format: {task_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "OK"}