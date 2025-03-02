import uvicorn
from fastapi import FastAPI
from ai_assistant.api.router import router as api_router
from ai_assistant.config.settings import settings

description = """
# AI Assistant API

This AI Assistant API leverages SmolagentS to provide intelligent responses to user queries.

## Capabilities

* **Chat**: Engage with the AI assistant through natural language
* **Web Search**: The assistant can search the web for information when needed
* **Context Awareness**: Maintain conversation context with conversation IDs

## Models

The service uses Azure OpenAI's GPT-4o-mini model for inference.
"""

tags_metadata = [
    {
        "name": "AI Assistant",
        "description": "Operations for interacting with the AI assistant",
    },
    {
        "name": "Health",
        "description": "API health check endpoints",
    },
]

app = FastAPI(
    title="Genova AI Assistant API",
    description=description,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
    contact={
        "name": "Support",
        "email": "support@example.com",
    },
)

app.include_router(api_router)


@app.get("/health", tags=["Health"], summary="Health check endpoint")
async def health_check():
    """
    Returns the current health status of the API.

    Returns:
        dict: A dictionary with the status field set to "healthy" if the API is functioning properly.
    """
    return {"status": "healthy"}


def main():
    uvicorn.run(
        "ai_assistant.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
