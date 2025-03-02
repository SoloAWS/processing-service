from pulsar.schema import AvroSchema, Record, String, Integer

# Schema definitions for event types
class ProcessingStartedSchema(Record):
    task_id = String()
    timestamp = String()
    image_type = String()
    region = String()
    priority = Integer(default=0)

class ProcessingCompletedSchema(Record):
    task_id = String()
    timestamp = String()
    status = String()
    message = String()
    region = String()

class ProcessingFailedSchema(Record):
    task_id = String()
    timestamp = String()
    error_message = String()
    region = String()

# Map event types to schemas
event_schemas = {
    "started": AvroSchema(ProcessingStartedSchema),
    "completed": AvroSchema(ProcessingCompletedSchema),
    "failed": AvroSchema(ProcessingFailedSchema)
}

# Convert domain events to schema objects
def event_to_schema_object(event):
    event_type = event.__class__.__name__.replace("Processing", "").lower()
    
    if event_type == "started":
        return ProcessingStartedSchema(
            task_id=str(event.task_id),
            timestamp=event.timestamp.isoformat(),
            image_type=event.metadata.image_type.value,
            region=event.metadata.region,
            priority=event.metadata.priority
        )
    elif event_type == "completed":
        return ProcessingCompletedSchema(
            task_id=str(event.task_id),
            timestamp=event.timestamp.isoformat(),
            status=event.result.status.value,
            message=event.result.message,
            region=event.region
        )
    elif event_type == "failed":
        return ProcessingFailedSchema(
            task_id=str(event.task_id),
            timestamp=event.timestamp.isoformat(),
            error_message=event.error_message,
            region=event.region
        )
    return None