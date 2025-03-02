from smolagents import (
    CodeAgent,
    LiteLLMModel,
)
from ai_assistant.config.settings import settings
from ai_assistant.agents.web_agent import web_agent
import os

# Create the model instance using settings from config
model = LiteLLMModel(
    model_id="azure/gpt-4o-mini",
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_base=settings.AZURE_OPENAI_ENDPOINT,
)

# Import the web agent after defining our model and agents


# Create a manager agent that coordinates other agents
manager_agent = CodeAgent(
    tools=[], model=model, managed_agents=[web_agent], max_steps=2
)


def get_agent():
    """Returns the manager agent to be used by the API."""
    return manager_agent
