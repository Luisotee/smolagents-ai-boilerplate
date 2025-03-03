from ai_assistant.prompts.manager import CUSTOM_CODE_SYSTEM_PROMPT
from smolagents import (
    CodeAgent,
    LiteLLMModel,
)
from smolagents.agents import populate_template
from ai_assistant.config.settings import settings
from ai_assistant.agents.web_agent import web_agent
import os

# Create the model instance using settings from config
model = LiteLLMModel(
    model_id="azure/gpt-4o-mini",
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_base=settings.AZURE_OPENAI_ENDPOINT,
)

# Define the empty tools dictionary - needed for the template
empty_tools = {}
empty_managed_agents = {"web_agent": web_agent}

# Populate the template with the bot name and empty tools/managed_agents
# (they will be properly populated by CodeAgent when initializing system prompt)
populated_system_prompt = populate_template(
    CUSTOM_CODE_SYSTEM_PROMPT,
    variables={
        "bot_name": settings.BOT_NAME,
        "authorized_imports": str(["os", "re", "json", "time"]),
        "tools": empty_tools,
        "managed_agents": empty_managed_agents,
    },
)

# Create proper prompt templates dictionary format expected by CodeAgent
custom_prompt_templates = {
    "system_prompt": populated_system_prompt,
    # Include empty default values for required nested dictionaries
    "planning": {
        "initial_facts": "",
        "initial_plan": "",
        "update_facts_pre_messages": "",
        "update_facts_post_messages": "",
        "update_plan_pre_messages": "",
        "update_plan_post_messages": "",
    },
    "managed_agent": {
        "task": "",
        "report": "",
    },
    "final_answer": {
        "pre_messages": "",
        "post_messages": "",
    },
}

# Create a manager agent that coordinates other agents
manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent],
    max_steps=3,
    prompt_templates=custom_prompt_templates,
    additional_authorized_imports=["os", "re", "json", "time"],
)


def get_agent():
    """Returns the manager agent to be used by the API."""
    return manager_agent
