from ai_assistant.prompts.formatting import get_formatting_guidelines
from smolagents import CodeAgent, LiteLLMModel
from ai_assistant.config.settings import settings
from ai_assistant.agents.tools import (
    ClinicGeneralInfoTool,
    ClinicPricingTool,
    ClinicServicesTool,
    ClinicStaffTool,
    ClinicAppointmentsTool,
)

# Create the model instance using settings from config
model = LiteLLMModel(
    model_id="azure/gpt-4o-mini",
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_base=settings.AZURE_OPENAI_ENDPOINT,
)


def get_agent(platform: str = "whatsapp", variables: dict = None):
    """
    Returns the manager agent to be used by the API.

    Args:
        platform: The platform name (e.g., "whatsapp", "telegram")
        variables: Optional variables to populate the template

    Returns:
        CodeAgent: The configured manager agent with appropriate formatting
    """
    # Get formatting guidelines for the specific platform
    formatting_guidelines = get_formatting_guidelines(platform)

    # Create a manager agent with all clinic tools
    manager_agent = CodeAgent(
        tools=[
            ClinicGeneralInfoTool(),
            ClinicPricingTool(),
            ClinicServicesTool(),
            ClinicStaffTool(),
            ClinicAppointmentsTool(),
        ],
        model=model,
        max_steps=7,
    )

    return manager_agent
