>>>> .env

PULSAR_SERVICE_URL=pulsar+ssl://pc-52a07d43.gcp-shared-usce1.g.snio.cloud:6651
PULSAR_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlMGRmYTU5LTdhZWItNTA5Ny1hMDFiLTJhMGFkMTgwNzFiMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsidXJuOnNuOnB1bHNhcjpvLWxnd3lwOnNuLWluc3RhbmNlIl0sImV4cCI6MTc0MzI5NTQxOSwiaHR0cHM6Ly9zdHJlYW1uYXRpdmUuaW8vc2NvcGUiOlsiYWRtaW4iLCJhY2Nlc3MiXSwiaHR0cHM6Ly9zdHJlYW1uYXRpdmUuaW8vdXNlcm5hbWUiOiJhZG1pbnNlcnZpY2VhY2NvdW50QG8tbGd3eXAuYXV0aC5zdHJlYW1uYXRpdmUuY2xvdWQiLCJpYXQiOjE3NDA3MDM0MjAsImlzcyI6Imh0dHBzOi8vcGMtNTJhMDdkNDMuZ2NwLXNoYXJlZC11c2NlMS5nLnNuaW8uY2xvdWQvYXBpa2V5cy8iLCJqdGkiOiIzMDI1OWRlNzFiMmI0YTFhOWExMmJhZTEzMTcxYWNiMSIsInBlcm1pc3Npb25zIjpbXSwic3ViIjoiRHV0bnVsN1NiTlpvbUFtd21UR0VCQ0JEMU5uaDZpc2hAY2xpZW50cyJ9.N0XAsTN4HRdDx-H2ncAhBVzs3xqw5f_Ir8j69qcnEKIyNmSCL789as-cRASyTFn4sfQVGFXfvYGIeno-0dtjvN5u1NutSlqhcb10wQjut_0Awh7KXmu1bPdb616YxBgE4CXgDygYagPQp2S66Sdxp0s8ghtDPmhNlpMeYzHRM3whBfxQ0tSpFNH2x82dNF6e3fKj7TW1X7C_Qh_tcw7xbUsUmZd1IjS8uFMeAOToVr5eO9NIXLjAKKMVgz10iEURbG84A20LLoaC14dZVXvUtQffm54CVxHUQJzhvVXfyijihkjuoxfVANxh-29OMAPdV_0YiNdS1nV3XRjp9nZytA
PULSAR_TOPIC=persistent://public/default/api-messages
PULSAR_SUBSCRIPTION=api-subscription



>>>> main.py example

import os
from typing import Dict, Any, List
import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pulsar
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Pulsar API", description="API for interacting with Apache Pulsar")

# Pulsar client configuration
PULSAR_SERVICE_URL = os.getenv("PULSAR_SERVICE_URL")
PULSAR_TOKEN = os.getenv("PULSAR_TOKEN")
PULSAR_TOPIC = os.getenv("PULSAR_TOPIC")
PULSAR_SUBSCRIPTION = os.getenv("PULSAR_SUBSCRIPTION")

# Data models
class Message(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class MessageResponse(BaseModel):
    message_id: str
    status: str = "sent"

class MessageList(BaseModel):
    messages: List[Message]

# Pulsar client setup
def get_pulsar_client():
    client = pulsar.Client(
        PULSAR_SERVICE_URL,
        authentication=pulsar.AuthenticationToken(PULSAR_TOKEN)
    )
    try:
        yield client
    finally:
        client.close()

# Producer setup
def get_producer(client: pulsar.Client = Depends(get_pulsar_client)):
    producer = client.create_producer(PULSAR_TOPIC)
    try:
        yield producer
    finally:
        producer.close()

# Consumer setup
def get_consumer(client: pulsar.Client = Depends(get_pulsar_client)):
    consumer = client.subscribe(
        PULSAR_TOPIC,
        PULSAR_SUBSCRIPTION,
        initial_position=pulsar.InitialPosition.Earliest
    )
    try:
        yield consumer
    finally:
        consumer.close()

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Pulsar API"}

@app.post("/messages", response_model=MessageResponse)
def send_message(message: Message, producer: pulsar.Producer = Depends(get_producer)):
    try:
        # Convert message to JSON string
        message_str = json.dumps(message.model_dump())
        
        # Send message to Pulsar
        message_id = producer.send(message_str.encode('utf-8'))
        
        # Return success response
        return MessageResponse(message_id=str(message_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@app.get("/messages", response_model=MessageList)
def receive_messages(count: int = 10, consumer: pulsar.Consumer = Depends(get_consumer)):
    messages = []
    try:
        for _ in range(count):
            # Set a timeout to avoid blocking indefinitely if there are no messages
            msg = consumer.receive(timeout_millis=5000)
            try:
                # Parse message content
                content = json.loads(msg.data().decode('utf-8'))
                messages.append(Message(**content))
                # Acknowledge the message
                consumer.acknowledge(msg)
            except Exception as e:
                # Negative acknowledge on error
                consumer.negative_acknowledge(msg)
                raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
    except pulsar.Timeout:
        # It's okay if we timeout, just return what we have
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to receive messages: {str(e)}")
    
    return MessageList(messages=messages)

@app.get("/health")
def health_check(client: pulsar.Client = Depends(get_pulsar_client)):
    return {"status": "healthy", "pulsar_connected": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



this is a really simple example of a fast api project that uses StreamNative pulsar and I want to implement this approach in my application

I want to use public tentand and default namespace let me know which actions and subscribers I need to create

for example I know some topics are processing.usa.started etc.. we can keep it simple and just use the 'started' event the failed and others we can omit for now

the whole idea is to remove pulsar from docker compose I don't want to use pulsar running on localhost instead I want to use pulsar running on StreamNative