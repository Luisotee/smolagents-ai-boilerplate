from ai_assistant.prompts.formatting import get_formatting_guidelines
from ai_assistant.prompts.manager import CUSTOM_CODE_SYSTEM_PROMPT
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, List
from ai_assistant.agents.manager import get_agent
from ai_assistant.utils.file_handler import FileHandler
from ai_assistant.database.supabase_client import supabase
from ai_assistant.config.settings import settings
import uuid
import datetime
from smolagents.local_python_executor import BASE_BUILTIN_MODULES
from smolagents.agents import populate_template

router = APIRouter(prefix="/api", tags=["AI Assistant"])


class Message(BaseModel):
    content: str = Field(
        ...,
        description="The message content to be processed by the AI assistant",
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID to maintain context between messages",
    )
    platform: str = Field(
        ...,
        description="The platform from which the message was sent",
    )
    platform_user_id: str = Field(
        ...,
        description="The user identifier from the platform",
    )
    attachment_paths: Optional[List[str]] = Field(
        default=[],
        description="List of paths to attached files",
    )


class Response(BaseModel):
    content: str = Field(..., description="The AI assistant's response message")
    conversation_id: str = Field(
        ..., description="The conversation ID for this interaction"
    )


@router.post(
    "/chat",
    response_model=Response,
    summary="Chat with the AI assistant",
    description="Send a message with optional attachments to the AI assistant",
)
async def chat(
    content: str = Form(...),  # Required
    platform: str = Form(...),  # Required
    platform_user_id: str = Form(...),  # Required
    conversation_id: Optional[str] = Form(None),  # Optional
    attachments: Optional[List[UploadFile]] = File(default=None),  # Optional
):
    """
    Chat with the AI assistant:

    - **content**: (Required) The message to send to the AI assistant
    - **platform**: (Required) The platform from which the message was sent
    - **platform_user_id**: (Required) The user identifier from the platform
    - **conversation_id**: (Optional) Identifier to maintain conversation context
    - **attachments**: (Optional) List of files to process
    """
    try:
        # Generate conversation_id if not provided
        if not conversation_id:
            conversation_id = f"conv-{uuid.uuid4()}"

        # Handle attachments if any
        attachment_paths = []
        if (
            attachments and attachments[0].filename
        ):  # Check if attachments are actually provided
            for attachment in attachments:
                file_path = await FileHandler.save_attachment(
                    attachment, conversation_id
                )
                attachment_paths.append(file_path)

        # Create message object
        message = Message(
            content=content,
            conversation_id=conversation_id,
            platform=platform,
            platform_user_id=platform_user_id,
            attachment_paths=attachment_paths,
        )

        # Get conversation history to provide context, using limit from settings
        try:
            user = supabase.get_user(platform, platform_user_id)

            # If user doesn't exist, create a new user
            if not user:
                user = supabase.get_or_create_user(platform, platform_user_id)

            history = []
            if user:
                history = supabase.get_conversation_history(
                    user_id=user["id"],
                    conversation_id=conversation_id,
                    limit=settings.MESSAGE_HISTORY_LIMIT,
                )
        except Exception as db_error:
            print(f"Database error: {db_error}")
            # Continue without history if there's a database error
            user = None
            history = []

        # Format history as structured data for the template
        conversation_history = []
        if history:
            # history is now already in pairs format
            for msg_pair in history:
                conversation_history.append(
                    {
                        "user": msg_pair.get("user_message", ""),
                        "assistant": msg_pair.get("assistant_response", ""),
                    }
                )

        # Get current time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format the message with timestamp and user name
        formatted_message = f"[{current_time}] André: {message.content}"

        # Process message - create agent with conversation history and attachments
        agent = get_agent(
            platform=platform,
            variables={
                "conversation_history": conversation_history,
                "attachment_paths": attachment_paths,
            },
        )

        # Set up the custom prompt with all required variables
        agent.prompt_templates["system_prompt"] = populate_template(
            CUSTOM_CODE_SYSTEM_PROMPT,
            variables={
                "conversation_history": conversation_history,
                "bot_name": settings.BOT_NAME,
                "formatting_guidelines": get_formatting_guidelines(platform),
                "tools": agent.tools,  # Changed from agent.tools_dict to agent.tools
                "authorized_imports": BASE_BUILTIN_MODULES,  # Add the authorized imports
                "managed_agents": {},  # Add empty managed_agents if needed by template
            },
        )

        # Then run the agent with the formatted message
        response_content = agent.run(formatted_message)

        # Store message and response in database
        try:
            if user:  # Only store if we have a valid user
                supabase.add_message_to_history(
                    platform=platform,
                    platform_user_id=platform_user_id,
                    message_content=content,
                    response_content=response_content,
                    conversation_id=conversation_id,
                )
        except Exception as store_error:
            print(f"Error storing message history: {store_error}")
            # Continue without storing the message if there's an error

        return Response(
            content=response_content, conversation_id=conversation_id
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
