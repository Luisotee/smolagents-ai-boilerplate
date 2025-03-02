import os
from pathlib import Path
from fastapi import UploadFile
from typing import List
import magic


class FileHandler:
    ALLOWED_MIME_TYPES = {
        # Documents
        "application/pdf": ".pdf",
        "application/msword": ".doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        # Audio
        "audio/wav": ".wav",
        "audio/ogg": ".ogg",
        "audio/mpeg": ".mp3",
        # Video
        "video/mp4": ".mp4",
        "video/mpeg": ".mpeg",
        # Images
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }

    @classmethod
    async def save_attachment(
        cls, file: UploadFile, conversation_id: str
    ) -> str:
        """
        Saves an uploaded file and returns its path
        """
        content_type = magic.from_buffer(await file.read(2048), mime=True)
        await file.seek(0)  # Reset file pointer

        if content_type not in cls.ALLOWED_MIME_TYPES:
            raise ValueError(f"Unsupported file type: {content_type}")

        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads") / conversation_id
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save file with original name
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return str(file_path)
