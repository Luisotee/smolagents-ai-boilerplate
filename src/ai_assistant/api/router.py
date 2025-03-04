from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, List
from ai_assistant.agents.manager import get_agent
from ai_assistant.utils.file_handler import FileHandler
from ai_assistant.database.supabase_client import supabase
from ai_assistant.config.settings import settings
import uuid

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

    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "What can you tell me about artificial intelligence?",
                "conversation_id": "conv-123456",
                "platform": "telegram",
                "platform_user_id": "12345678",
                "attachment_paths": [],
            }
        }
    }


class Response(BaseModel):
    content: str = Field(..., description="The AI assistant's response message")
    conversation_id: str = Field(
        ..., description="The conversation ID for this interaction"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "Artificial intelligence (AI) refers to the simulation of human intelligence processes by machines...",
                "conversation_id": "conv-123456",
            }
        }
    }


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
        history = supabase.get_conversation_history(
            platform=platform,
            platform_user_id=platform_user_id,
            conversation_id=conversation_id,
            limit=settings.MESSAGE_HISTORY_LIMIT,  # Use the configured limit
        )

        # Format history for context if any exists
        context = ""
        if history:
            context = "Previous conversation:\n"
            for i, msg in enumerate(reversed(history)):  # Oldest first
                context += f"User: {msg['user_message']}\n"
                context += f"Assistant: {msg['assistant_response']}\n"
            context += "\nCurrent message:\n"

        # Add context to the message content if we have history
        prompt = (
            f"{context}\nUser: {message.content}"
            if context
            else message.content
        )

        # Process message
        agent = get_agent(
            platform
        )  # Pass the platform to get platform-specific formatting
        response_content = agent.run(prompt)

        # Store message and response in database
        supabase.add_message_to_history(
            platform=platform,
            platform_user_id=platform_user_id,
            message_content=content,
            response_content=response_content,
            conversation_id=conversation_id,
        )

        return Response(
            content=response_content, conversation_id=conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
