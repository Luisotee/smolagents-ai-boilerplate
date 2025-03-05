from smolagents import (
    CodeAgent,
    LiteLLMModel,
)
from smolagents.agents import populate_template
from ai_assistant.config.settings import settings
from ai_assistant.prompts.clinic_info import CLINIC_INFO_SYSTEM_PROMPT
from ai_assistant.agents.tools.clinick_knowledge import ClinicKnowledgeTool

# Create the model instance using OpenRouter
model = LiteLLMModel(
    model_id="azure/gpt-4o-mini",
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_base=settings.AZURE_OPENAI_ENDPOINT,
)

# Create the clinic knowledge tool
clinic_knowledge_tool = ClinicKnowledgeTool()

# Define tools and empty managed agents dictionaries for template
tools = {"clinic_knowledge": clinic_knowledge_tool}
empty_managed_agents = {}

# Populate the template with tools and empty managed_agents
populated_system_prompt = populate_template(
    CLINIC_INFO_SYSTEM_PROMPT,
    variables={
        "formatting_guidelines": "",  # Empty string instead of formatting guidelines
        "tools": tools,
        "managed_agents": empty_managed_agents,
        "authorized_imports": str(["os", "re", "json", "time"]),
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

# Create the clinic info agent
clinic_info_agent = CodeAgent(
    tools=[clinic_knowledge_tool],  # Add the tool to the agent
    model=model,
    name="clinic_info",
    description="Provides accurate information about Clínica Bella's services, procedures, location, and policies.",
    # prompt_templates=custom_prompt_templates,
    max_steps=2,
)


def get_clinic_info_agent():
    """Returns the clinic information agent."""
    return clinic_info_agent
