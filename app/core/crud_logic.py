import os
from fastapi import HTTPException
from app.constants import FILES_EXTENSIONS, BASE_FOR_EXTENSION
from app.schemas import FileRequest


def get_file_path(file_name: str, file_type: str) -> str:
    if file_type not in FILES_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"The {file_type} files are not available for this function",
        )

    assigned_base = BASE_FOR_EXTENSION[file_type]
    assigned_extension = FILES_EXTENSIONS[file_type]

    return os.path.join(assigned_base, file_name + assigned_extension)


def read_file_content(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {error} detected when tried to read the content of the file",
        )


def write_file_content(file_path: str, content: str) -> None:
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {error} detected when tried to write to the file",
        )


def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def delete_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(file_path)
