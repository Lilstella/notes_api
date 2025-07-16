import os
from fastapi import APIRouter, HTTPException
from app.schemas import (
    MarkdownContent,
    MarkdownResponse,
    MarkdownVersionsResponse,
    MarkdownVersionResponse,
)
from app.constants import MARKDOWN_BASE_DIR
from app.core.versioning import (
    save_version,
    list_versions,
    read_version,
    delete_versions,
)

os.makedirs(MARKDOWN_BASE_DIR, exist_ok=True)
router = APIRouter()


def get_markdown_file_path(filename: str) -> str:
    return os.path.join(MARKDOWN_BASE_DIR, filename + ".md")


@router.get("/{filename}", response_model=MarkdownResponse)
def get_markdown(filename: str) -> MarkdownResponse:
    file_path = get_markdown_file_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return MarkdownResponse(filename=filename, content=content)


@router.post("/{filename}")
def create_markdown(filename: str, content: MarkdownContent) -> dict[str, str]:
    file_path = get_markdown_file_path(filename)

    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File already exists")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content.text)

    return {"message": "File created successfully"}


@router.put("/{filename}")
def update_markdown(filename: str, content: MarkdownContent) -> dict[str, str]:
    try:
        current = get_markdown(filename)
        save_version(filename, current.content)
    except FileNotFoundError:
        pass

    file_path = get_markdown_file_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content.text)

    return {"message": "File updated successfully"}


@router.delete("/{filename}")
def delete_markdown(filename: str) -> dict[str, str]:
    file_path = get_markdown_file_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    delete_versions(filename)

    return {"message": "File deleted successfully"}


@router.get("/{file_name}/versions")
def get_markdown_versions(file_name: str) -> MarkdownVersionsResponse:
    list_of_versions = list_versions(file_name)
    return MarkdownVersionsResponse(filename=file_name, versions=list_of_versions)


@router.get("/{file_name}/versions/{version}")
def get_markdown_version(file_name: str, version: str) -> MarkdownVersionResponse:
    try:
        content = read_version(file_name, version)
        return MarkdownVersionResponse(
            filename=file_name, version=version, content=content
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Version not found")
