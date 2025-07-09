import os
import shutil
from fastapi import APIRouter, HTTPException
from app.schemas import ImportFileRequest
from app.constants import BASE_DIR, MARKDOWN_BASE_DIR, MARKDOWN

router = APIRouter()

# Asegura que existan las carpetas base
os.makedirs(BASE_DIR, exist_ok=True)

@router.post("/")
def import_file(request: ImportFileRequest):
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    extension = os.path.splitext(request.file_path)[1].lower()
    file_name = os.path.basename(request.file_path)

    match extension:
        case MARKDOWN:
            destination = os.path.join(MARKDOWN_BASE_DIR, file_name)

            if os.path.abspath(request.file_path) == os.path.abspath(destination):
                raise HTTPException(status_code=400, detail="File is already in storage")

            shutil.copy(request.file_path, destination)
            return {
                "message": "Markdown file imported successfully",
                "filename": file_name,
                "stored_at": destination
            }
        case _:
            raise HTTPException(status_code=400, detail="Unsupported file extension")
