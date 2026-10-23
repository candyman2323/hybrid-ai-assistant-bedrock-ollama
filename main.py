
import logging
import os

import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "amazon.nova-micro-v1:0"
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434"
).rstrip("/")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)

app = FastAPI(title="Hybrid AI Assistant")
@app.get("/ui")
def chat_ui():
    return FileResponse("index.html")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    provider: str = Field(default="auto")


def choose_provider(message: str) -> str:
    """Simple rule-based model selection."""
    text = message.lower()

    cloud_keywords = [
        "compare",
        "architecture",
        "design",
        "debug",
        "analyze",
        "analyse",
        "step by step",
        "explain in detail",
        "migration",
        "deploy"
    ]

    if len(message) > 250:
        return "bedrock"

    if any(word in text for word in cloud_keywords):
        return "bedrock"

    return "local"


def ask_local(message: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "user", "content": message}
            ],
            "stream": False
        },
        timeout=(5, 120)
    )

    response.raise_for_status()
    return response.json()["message"]["content"]


def ask_bedrock(message: str) -> str:
    response = bedrock.converse(
        modelId=BEDROCK_MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": message}]
            }
        ],
        inferenceConfig={
            "maxTokens": 600,
            "temperature": 0.4
        }
    )

    return response["output"]["message"]["content"][0]["text"]


@app.get("/")
def home():
    return {
        "application": "Hybrid AI Assistant",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "llama3.2",
                "object": "model",
                "owned_by": "ollama"
            },
            {
                "id": "amazon.nova-micro-v1:0",
                "object": "model",
                "owned_by": "bedrock"
            }
        ]
    }



@app.post("/chat")
def chat(request: ChatRequest):
    provider = request.provider.lower().strip()

    if provider not in ("local", "bedrock", "auto"):
        raise HTTPException(
            status_code=400,
            detail="provider must be local, bedrock, or auto"
        )

    if provider == "auto":
        provider = choose_provider(request.message)

    try:
        if provider == "local":
            answer = ask_local(request.message)
        else:
            answer = ask_bedrock(request.message)

        return {
            "provider": provider,
            "answer": answer
        }

    except requests.RequestException:
        logger.exception("Ollama request failed")
        raise HTTPException(
            status_code=502,
            detail="Could not reach Ollama. Check that it is running."
        )

    except (ClientError, BotoCoreError):
        logger.exception("Bedrock request failed")
        raise HTTPException(
            status_code=502,
            detail=(
                "Bedrock request failed. Check AWS credentials, "
                "model ID, Region, and IAM permissions."
            )
        )

    except (KeyError, IndexError, TypeError):
        logger.exception("Unexpected model response")
        raise HTTPException(
            status_code=502,
            detail="The AI model returned an unexpected response."
        )
