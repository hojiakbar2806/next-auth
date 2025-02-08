from pathlib import Path
from fastapi import UploadFile, HTTPException
import mimetypes


def save_image(file: UploadFile, file_name: str, file_path: str) -> str:
    try:
        content_type = file.content_type
        file_extension = mimetypes.guess_extension(content_type)

        if not file_extension:
            raise HTTPException(
                status_code=400, detail="Unsupported file type")

        full_file_name = f"{file_name}{file_extension}"

        save_path = Path("images") / file_path / full_file_name
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with save_path.open("wb") as buffer:
            buffer.write(file.file.read())

        return f"images/{file_path}/{full_file_name}"
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in save image: {e}"
        )
