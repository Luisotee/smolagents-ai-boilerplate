from smolagents import (
    CodeAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool,
)
from ai_assistant.config.settings import settings
import os

# Create the model instance
model = LiteLLMModel(
    model_id="azure/gpt-4o-mini",
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_base=settings.AZURE_OPENAI_ENDPOINT,
)

# Initialize the web browsing agent with webpage visiting tool
web_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    name="web_agent",
    description="Runs web searches for you. Give it your query as an argument.",
)


def get_web_agent():
    """Returns the web browsing agent."""
    return web_agent
