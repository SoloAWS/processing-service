FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV NEW_RELIC_LICENSE_KEY="c63692e68d76eb75e86aee91a8b49c77FFFFNRAL"
ENV NEW_RELIC_APP_NAME="processing-service"
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG=stdout

CMD ["newrelic-admin", "run-program", "uvicorn", "src.processing_service.main:app", "--host", "0.0.0.0", "--port", "8080"]