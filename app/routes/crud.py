import os
from fastapi import APIRouter, HTTPException, status
from app.constants import BASE_DIR, BASE_FOR_EXTENSION
from app.schemas import FileRequest, FileResponse
from app.core.versioning import save_version, delete_versions
from app.core.crud_logic import (
    get_file_path,
    read_file_content,
    write_file_content,
    ensure_directory_exists,
    file_exists,
    delete_file,
)

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

router = APIRouter()


@router.get("/{file_name}", response_model=FileResponse)
def get_file(file_name: str, file_type: str) -> FileResponse:
    file_path = get_file_path(file_name, file_type)

    content = read_file_content(file_path)

    return FileResponse(filename=file_name, content=content, filetype=file_type)


@router.post("/create/{file_name}", status_code=status.HTTP_201_CREATED)
def create_file(file_name: str, content: FileRequest) -> dict[str, str]:
    request_file_type = content.filetype
    file_path = get_file_path(file_name, request_file_type)

    if file_exists(file_path):
        raise HTTPException(
            status_code=400, detail=f"The file {file_name} already exists"
        )

    ensure_directory_exists(BASE_FOR_EXTENSION[request_file_type])

    write_file_content(file_path, content.text)

    return {"message": f"The file {file_name} was created successfully"}


@router.put("/edit/{filename}")
def update_file(filename: str, content: FileRequest) -> dict[str, str]:
    try:
        current = get_file(filename, content.filetype)
        save_version(filename, current.content, content.filetype)
    except OSError as error:
        raise HTTPException(status_code=500, detail=f"Error: {error}")
    except FileNotFoundError:
        pass

    file_path = get_file_path(filename, content.filetype)

    if not file_exists(file_path):
        raise HTTPException(status_code=404, detail=f"The file {filename} not found")

    write_file_content(file_path, content.text)

    return {"message": "File updated successfully"}


@router.delete("/delete/{filename}")
def delete_file_type(filename: str, file_type: str) -> dict[str, str]:
    file_path = get_file_path(filename, file_type)

    delete_file(file_path)
    delete_versions(filename, file_type)

    return {"message": "File deleted successfully"}
