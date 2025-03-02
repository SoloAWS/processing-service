import uvicorn
from fastapi import FastAPI
from src.processing_service.modules.latam_processing.infrastructure.consumers import (
    LatamProcessingConsumer,
)
from src.processing_service.modules.usa_processing.infrastructure.consumers import (
    UsaProcessingConsumer,
)
from src.processing_service.modules.processing.api.api import app as processing_app
from src.processing_service.config.database import init_models
from src.processing_service.config.settings import Settings

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

settings = Settings()

app = FastAPI(title="Processing Service")

# Set up OpenTelemetry
resource = Resource.create({"service.name": "processing-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configure Cloud Trace exporter
cloud_trace_exporter = CloudTraceSpanExporter()
span_processor = BatchSpanProcessor(cloud_trace_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Mount the processing module
app.mount("/processing", processing_app)

# Initialize consumers with StreamNative Pulsar
app.state.latam_consumer = LatamProcessingConsumer()
app.state.usa_consumer = UsaProcessingConsumer()


@app.on_event("startup")
async def startup_event():
    # Initialize database models
    await init_models()

    # Start consumers
    await app.state.latam_consumer.subscribe()
    await app.state.usa_consumer.subscribe()


@app.on_event("shutdown")
async def shutdown_event():
    # Close consumers
    app.state.latam_consumer.close()
    app.state.usa_consumer.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
