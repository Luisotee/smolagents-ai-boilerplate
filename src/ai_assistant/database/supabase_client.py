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

    def get_user(self, platform: str, platform_user_id: str) -> Optional[Dict]:
        """Get user by platform and platform_user_id"""
        response = (
            self.client.table(self.users_table)
            .select("*")
            .eq(f"{platform}_id", platform_user_id)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None

    def create_user(
        self, platform: str, platform_user_id: str, name: Optional[str] = None
    ) -> Dict:
        """Create a new user"""
        user_data = {
            f"{platform}_id": platform_user_id,
            "name": name,
            "message_history": json.dumps([]),
        }

        response = (
            self.client.table(self.users_table).insert(user_data).execute()
        )

        return response.data[0]

    def get_or_create_user(
        self, platform: str, platform_user_id: str, name: Optional[str] = None
    ) -> Dict:
        """Get user or create if not exists"""
        user = self.get_user(platform, platform_user_id)
        if not user:
            user = self.create_user(platform, platform_user_id, name)
        return user

    def add_message_to_history(
        self,
        platform: str,
        platform_user_id: str,
        message_content: str,
        response_content: str,
        conversation_id: str,
    ) -> Dict:
        """Add message and response to user history"""
        user = self.get_or_create_user(platform, platform_user_id)
        user_id = user["id"]

        # Parse existing message history or create empty list
        try:
            message_history = json.loads(user.get("message_history", "[]"))
        except (json.JSONDecodeError, TypeError):
            message_history = []

        # Append new message and response
        timestamp = datetime.now().isoformat()
        message_history.append(
            {
                "timestamp": timestamp,
                "conversation_id": conversation_id,
                "user_message": message_content,
                "assistant_response": response_content,
            }
        )

        # Update the user record
        response = (
            self.client.table(self.users_table)
            .update(
                {
                    "message_history": json.dumps(message_history),
                    "last_updated_at": timestamp,
                }
            )
            .eq("id", user_id)
            .execute()
        )

        return response.data[0]

    def get_conversation_history(
        self,
        platform: str,
        platform_user_id: str,
        conversation_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict]:
        """Get conversation history for a user"""
        user = self.get_user(platform, platform_user_id)
        if not user:
            return []

        try:
            message_history = json.loads(user.get("message_history", "[]"))
        except (json.JSONDecodeError, TypeError):
            return []

        # Filter by conversation_id if provided
        if conversation_id:
            message_history = [
                msg
                for msg in message_history
                if msg.get("conversation_id") == conversation_id
            ]

        # Return most recent messages first, limited by limit
        return sorted(
            message_history, key=lambda x: x.get("timestamp", ""), reverse=True
        )[:limit]


# Create a singleton instance
supabase = SupabaseClient()
