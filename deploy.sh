#!/bin/bash

# Configura las variables de entorno
export PROJECT_ID="sologcp"
export APP_NAME="processing-app"
export PORT=8080
export REGION="us-central1"
export IMAGE_TAG="gcr.io/$PROJECT_ID/$APP_NAME"

# Lee variables de entorno del archivo .env
if [ -f .env ]; then
  source .env
else
  echo "Error: .env file not found"
  exit 1
fi

# Establece el proyecto por defecto
gcloud config set project $PROJECT_ID

# Habilita los servicios necesarios
gcloud services enable cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    run.googleapis.com

# Construye la imagen de Docker y súbela a Google Container Registry
gcloud builds submit --tag $IMAGE_TAG

# Despliega la aplicación en Google Cloud Run con variables de entorno
gcloud run deploy $APP_NAME \
    --image $IMAGE_TAG \
    --platform managed \
    --region $REGION \
    --port $PORT \
    --set-env-vars="DATABASE_URL=${DATABASE_URL},PULSAR_SERVICE_URL=${PULSAR_SERVICE_URL},PULSAR_TOKEN=${PULSAR_TOKEN}" \
    --allow-unauthenticated

echo "Deployment complete!"