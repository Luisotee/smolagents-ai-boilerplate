from smolagents import (
    CodeAgent,
    LiteLLMModel,
)
from smolagents.agents import populate_template
from ai_assistant.config.settings import settings
from ai_assistant.agents.tools.clinick_knowledge import ClinicKnowledgeTool

# Create the model instance using OpenRouter
model = LiteLLMModel(
    model_id="openrouter/deepseek/deepseek-chat:free",
    api_key=settings.OPEN_ROUTER_API_KEY,  # Use the OpenRouter API key
)

# Create the clinic info agent
clinic_info_agent = CodeAgent(
    tools=[ClinicKnowledgeTool()],  # Add the tool to the agent
    model=model,
    name="clinic_info",
    description="Provides information about Bella clinic.",
    # prompt_templates=custom_prompt_templates,
)


def get_clinic_info_agent():
    """Returns the clinic information agent."""
    return clinic_info_agent
