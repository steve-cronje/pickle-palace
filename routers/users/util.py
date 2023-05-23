from fastapi import UploadFile
from pathlib import Path
import shutil

def save_upload_file(upload_file: UploadFile, username) -> str:
    destination = f"media/users/{username}/images/{upload_file.filename}"
    path = Path(destination)
    try:
        with path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    return str(path).removeprefix("media")