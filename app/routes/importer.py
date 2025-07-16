import os
import shutil
from fastapi import APIRouter, HTTPException
from app.schemas import ImportFileRequest
from app.constants import BASE_FOR_EXTENSION, BASE_DIR

router = APIRouter()

os.makedirs(BASE_DIR, exist_ok=True)


@router.post("/")
def import_file(request: ImportFileRequest) -> dict[str, str]:
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    extension = os.path.splitext(request.file_path)[1].lower()
    file_name = os.path.basename(request.file_path)

    if extension not in BASE_FOR_EXTENSION.keys():
        raise HTTPException(status_code=400, detail="Invalid file extension")

    base_dir = BASE_FOR_EXTENSION[extension]
    os.makedirs(base_dir, exist_ok=True)

    destination_path = os.path.join(base_dir, file_name)
    if os.path.exists(destination_path):
        raise HTTPException(status_code=409, detail="File already exists")

    shutil.copy(request.file_path, destination_path)

    return {
        "message": "File imported successfully",
        "destination_path": destination_path,
        "file_name": file_name,
    }
