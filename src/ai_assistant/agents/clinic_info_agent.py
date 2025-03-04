from smolagents import (
    CodeAgent,
    LiteLLMModel,
)
from smolagents.agents import populate_template
from ai_assistant.config.settings import settings
from ai_assistant.prompts.clinic_info import CLINIC_INFO_SYSTEM_PROMPT
from ai_assistant.prompts.formatting import get_formatting_guidelines

# Create the model instance
model = LiteLLMModel(
    model_id="azure/gpt-4o-mini",
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_base=settings.AZURE_OPENAI_ENDPOINT,
)

# Get default formatting guidelines (WhatsApp)
formatting_guidelines = get_formatting_guidelines("whatsapp")

# Populate the template with formatting guidelines
populated_system_prompt = populate_template(
    CLINIC_INFO_SYSTEM_PROMPT,
    variables={
        "formatting_guidelines": formatting_guidelines,
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
    tools=[],  # No tools needed for this information agent
    model=model,
    name="clinic_info",
    description="Provides accurate information about Clínica Bella's services, procedures, location, and policies.",
    prompt_templates=custom_prompt_templates,
)


def get_clinic_info_agent():
    """Returns the clinic information agent."""
    return clinic_info_agent
