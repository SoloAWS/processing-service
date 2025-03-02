from dataclasses import dataclass
import uuid
from ...domain.repositories import ProcessingRepository
from .....seedwork.application.queries import Query, QueryResult, QueryHandler
from ...domain.entities import ProcessingTask


@dataclass
class GetTaskStatusQuery(Query):
    task_id: uuid.UUID


@dataclass
class TaskStatusDTO:
    id: str
    status: str
    message: str
    started_at: str = None
    completed_at: str = None


class GetTaskStatusHandler(QueryHandler):
    def __init__(self, repository: ProcessingRepository):
        self.repository = repository

    async def handle(self, query: GetTaskStatusQuery) -> QueryResult[TaskStatusDTO]:
        task = await self.repository.get_by_id(query.task_id)

        if not task:
            return QueryResult(None)

        return QueryResult(
            TaskStatusDTO(
                id=str(task.id),
                status=task.result.status.value if task.result else "PENDING",
                message=task.result.message if task.result else "",
                started_at=task.started_at.isoformat() if task.started_at else None,
                completed_at=(
                    task.completed_at.isoformat() if task.completed_at else None
                ),
            )
        )
