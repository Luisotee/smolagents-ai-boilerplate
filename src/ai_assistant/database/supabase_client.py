from supabase import create_client
from ai_assistant.config.settings import settings
import json
from datetime import datetime
from typing import List, Dict, Optional, Any


class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client"""
        self.client = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_KEY
        )
        self.users_table = settings.SUPABASE_USERS_TABLE
        self.messages_table = "messages"  # Table for messages

    def get_user(self, platform: str, platform_user_id: str) -> Optional[Dict]:
        """Get user by platform and platform_user_id"""
        # Use the correct column name based on platform
        column_name = f"{platform}_id"

        try:
            response = (
                self.client.table(self.users_table)
                .select("*")
                .eq(column_name, platform_user_id)
                .execute()
            )

            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error retrieving user: {e}")
            # If there's an error, we'll return None so a new user can be created
            return None

    def create_user(
        self,
        platform: str,
        platform_user_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Dict:
        """Create a new user"""
        user_data = {
            f"{platform}_id": platform_user_id,
            "name": name,
            "email": email,
            "phone": phone,
        }

        response = (
            self.client.table(self.users_table).insert(user_data).execute()
        )

        return response.data[0]

    def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict:
        """Update user data"""
        response = (
            self.client.table(self.users_table)
            .update(data)
            .eq("id", user_id)
            .execute()
        )

        return response.data[0]

    def get_or_create_user(
        self,
        platform: str,
        platform_user_id: str,
        user_info: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Get user or create if not exists"""
        user = self.get_user(platform, platform_user_id)

        if not user:
            # Create new user with any provided info
            user_data = {f"{platform}_id": platform_user_id}
            if user_info:
                user_data.update(user_info)
            user = self.create_user(
                platform,
                platform_user_id,
                name=user_info.get("name") if user_info else None,
                email=user_info.get("email") if user_info else None,
                phone=user_info.get("phone") if user_info else None,
            )
        elif user_info:
            # Update existing user with new info if provided
            user = self.update_user(user["id"], user_info)

        return user

    def get_user_message_record(self, user_id: str) -> Optional[Dict]:
        """Get the user's message record or None if it doesn't exist"""
        response = (
            self.client.table(self.messages_table)
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None

    def create_message_record(self, user_id: str) -> Dict:
        """Create a new message record for user with empty content"""
        message_data = {
            "user_id": user_id,
            "content": [],  # Change to an empty array instead of nested structure
        }

        response = (
            self.client.table(self.messages_table)
            .insert(message_data)
            .execute()
        )

        return response.data[0]

    def get_or_create_message_record(self, user_id: str) -> Dict:
        """Get or create message record for user"""
        record = self.get_user_message_record(user_id)

        if not record:
            record = self.create_message_record(user_id)

        return record

    def add_message_to_history(
        self,
        platform: str,
        platform_user_id: str,
        message_content: str,
        response_content: str,
        conversation_id: Optional[
            str
        ] = None,  # We'll keep this param for backward compatibility
    ) -> Dict[str, Any]:
        """
        Store both user message and assistant response in the user's message history.
        This implementation keeps one row per user with a flat array of messages in the JSONB column.

        Args:
            platform: Platform identifier (e.g., "whatsapp", "telegram")
            platform_user_id: User ID from the platform
            message_content: Content of the user message
            response_content: Content of the assistant response
            conversation_id: Optional conversation identifier (not used in flat structure)

        Returns:
            Dict containing the recorded exchange information
        """
        try:
            # Get or create the user
            user = self.get_or_create_user(platform, platform_user_id)
            user_id = user["id"]

            # Get or create the message record
            message_record = self.get_or_create_message_record(user_id)

            # Prepare new message exchange
            timestamp = datetime.now().isoformat()
            new_exchange = {
                "user_message": message_content,
                "assistant_response": response_content,
                "timestamp": timestamp,
            }

            # Get existing content - either an array or initialize as empty array
            content = message_record.get("content", [])
            if not isinstance(content, list):
                # Handle case where content might be in old format
                content = []

            # Add new exchange to the array
            content.append(new_exchange)

            # Update the message record
            updated_data = {"content": content}
            response = (
                self.client.table(self.messages_table)
                .update(updated_data)
                .eq("id", message_record["id"])
                .execute()
            )

            return {
                "user": user,
                "conversation_id": "default",  # Always return default
                "timestamp": timestamp,
                "success": True,
            }
        except Exception as e:
            print(f"Error adding message to history: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def get_conversation_history(
        self,
        user_id: str,
        conversation_id: Optional[
            str
        ] = None,  # We'll keep this param for backward compatibility
        limit: int = 10,
    ) -> List[Dict]:
        """
        Get conversation history for a user.

        Args:
            user_id: The user ID
            conversation_id: Optional conversation ID (not used in flat structure)
            limit: Maximum number of exchanges to return

        Returns:
            List of message exchanges (user message and assistant response pairs)
        """
        try:
            # Get the message record
            message_record = self.get_user_message_record(user_id)

            if not message_record or "content" not in message_record:
                return []

            content = message_record.get("content", [])

            # Handle if content is not an array (old format)
            if not isinstance(content, list):
                # Try to extract from old format if possible
                try:
                    conversations = content.get("conversations", {})
                    all_exchanges = []
                    for exchanges in conversations.values():
                        all_exchanges.extend(exchanges)
                    # Sort by timestamp (most recent first)
                    all_exchanges.sort(
                        key=lambda x: x.get("timestamp", ""), reverse=True
                    )
                    return all_exchanges[:limit]
                except:
                    return []

            # Return the most recent exchanges up to the limit
            # Sort by timestamp (most recent first)
            content.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

            # Return the limited number of messages
            return content[:limit]

        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def get_user_by_platform_id(
        self, platform: str, platform_user_id: str
    ) -> Optional[Dict]:
        """Get user by platform ID"""
        return self.get_user(platform, platform_user_id)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Find a user by email"""
        response = (
            self.client.table(self.users_table)
            .select("*")
            .eq("email", email)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None

    def get_user_by_phone(self, phone: str) -> Optional[Dict]:
        """Find a user by phone number"""
        response = (
            self.client.table(self.users_table)
            .select("*")
            .eq("phone", phone)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None


# Create a singleton instance
supabase = SupabaseClient()
