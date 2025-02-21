# src/processing_service/modules/processing/api/api.py
from fastapi import FastAPI, HTTPException, UploadFile, Depends
from pydantic import BaseModel
from typing import Optional
import uuid
from ..application.commands.process_image import (
    ProcessImageCommand,
    ProcessImageHandler,
)
from ..application.queries.get_task_status import (
    GetTaskStatusQuery,
    GetTaskStatusHandler,
)
from ..domain.value_objects import ImageType

app = FastAPI(title="Processing Service")


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


# Dependency injection handlers
async def get_command_handler() -> ProcessImageHandler:
    # Here we would normally use a proper DI container
    # For now, we'll create handler with mock dependencies
    return ProcessImageHandler(repository=None)


async def get_query_handler() -> GetTaskStatusHandler:
    # Here we would normally use a proper DI container
    return GetTaskStatusHandler(repository=None)


@app.post("/process", response_model=ProcessingResponse)
async def process_image(
    request: ProcessImageRequest,
    file: UploadFile,
    command_handler: ProcessImageHandler = Depends(get_command_handler),
):
    try:
        # Validate image type
        if request.image_type not in ImageType.__members__:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image type. Must be one of: {list(ImageType.__members__.keys())}",
            )

        # Read file content
        content = await file.read()

        # Create and execute command
        command = ProcessImageCommand(
            image_type=request.image_type,
            region=request.region,
            raw_data=content,
            priority=request.priority,
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
