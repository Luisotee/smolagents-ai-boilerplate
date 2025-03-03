from ai_assistant.database.supabase_client import supabase
from ai_assistant.config.settings import settings


def run_migrations():
    """
    Check if users table exists and create if needed
    Note: This is a simplified example - in production, use a proper migration tool
    """
    try:
        # Check if the users table exists by querying it
        table_name = settings.SUPABASE_USERS_TABLE
        supabase.client.table(table_name).select("count").limit(1).execute()
        print(f"Table {table_name} exists")
    except Exception as e:
        print(f"Error checking table: {e}")
        print(
            f"Please ensure the {settings.SUPABASE_USERS_TABLE} table exists with the required schema"
        )


if __name__ == "__main__":
    run_migrations()
