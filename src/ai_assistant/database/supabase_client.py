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
        self.messages_table = "messages"  # New table for messages

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

    def store_message(
        self,
        user_id: str,
        message_content: str,
        is_from_user: bool = True,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Store a message in the messages table"""
        content = {
            "text": message_content,
            "timestamp": datetime.now().isoformat(),
            "from_user": is_from_user,
            "conversation_id": conversation_id,
        }

        # Add any additional metadata
        if metadata:
            content.update(metadata)

        message_data = {"user_id": user_id, "content": content}

        response = (
            self.client.table(self.messages_table)
            .insert(message_data)
            .execute()
        )

        return response.data[0]

    def add_conversation_exchange(
        self,
        platform: str,
        platform_user_id: str,
        user_message: str,
        assistant_response: str,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a complete exchange (user message and assistant response)"""
        # Get or create the user
        user = self.get_or_create_user(platform, platform_user_id)
        user_id = user["id"]

        # Store the user message
        self.store_message(
            user_id=user_id,
            message_content=user_message,
            is_from_user=True,
            conversation_id=conversation_id,
        )

        # Store the assistant response
        response_data = self.store_message(
            user_id=user_id,
            message_content=assistant_response,
            is_from_user=False,
            conversation_id=conversation_id,
        )

        return {
            "user": user,
            "exchange_recorded": True,
            "response_id": response_data["id"],
        }

    def get_conversation_history(
        self,
        user_id: str,
        conversation_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict]:
        """Get conversation history for a user"""
        query = (
            self.client.table(self.messages_table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
        )

        # Filter by conversation_id if provided
        if conversation_id:
            # Since conversation_id is inside JSONB, we need to use contains operator
            query = query.filter(
                "content->conversation_id", "eq", conversation_id
            )

        response = query.execute()

        return response.data if response.data else []

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
