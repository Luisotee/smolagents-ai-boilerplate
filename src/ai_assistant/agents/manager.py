from ai_assistant.prompts.manager import CUSTOM_CODE_SYSTEM_PROMPT
from ai_assistant.prompts.formatting import get_formatting_guidelines
from smolagents import (
    CodeAgent,
    LiteLLMModel,
)
from smolagents.agents import populate_template
from ai_assistant.config.settings import settings
from ai_assistant.agents.clinic_info_agent import clinic_info_agent
import os
import datetime

# Create the model instance using settings from config
model = LiteLLMModel(
    model_id="openrouter/deepseek/deepseek-chat:free",
    api_key=settings.OPEN_ROUTER_API_KEY,  # Use the OpenRouter API key
)

# Define the empty tools dictionary - needed for the template
empty_tools = {}
empty_managed_agents = {
    "clinic_info": clinic_info_agent,
}

# Get default formatting guidelines (WhatsApp)
formatting_guidelines = get_formatting_guidelines("whatsapp")

# Populate the template with the bot name and empty tools/managed_agents
# (they will be properly populated by CodeAgent when initializing system prompt)
populated_system_prompt = populate_template(
    CUSTOM_CODE_SYSTEM_PROMPT,
    variables={
        "bot_name": settings.BOT_NAME,
        "authorized_imports": str(["os", "re", "json", "time", "datetime"]),
        "tools": empty_tools,
        "managed_agents": empty_managed_agents,
        "formatting_guidelines": formatting_guidelines,
        "conversation_history": [],
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_name": "André",
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
    managed_agents=[
        clinic_info_agent,
    ],
    prompt_templates=custom_prompt_templates,
    additional_authorized_imports=["os", "re", "json", "time", "datetime"],
)


def get_agent(platform: str = "whatsapp"):
    """
    Returns the manager agent to be used by the API.

    Args:
        platform: The platform name (e.g., "whatsapp", "telegram")

    Returns:
        CodeAgent: The configured manager agent with appropriate formatting
    """
    # If we want to dynamically update formatting based on platform
    # we would need to recreate the agent here with updated formatting
    return manager_agent
