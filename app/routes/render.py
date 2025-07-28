import os
from fastapi import APIRouter, HTTPException
from app.core.rendering import to_html, to_markdown
from app.constants import BASE_FOR_EXTENSION, FILES_EXTENSIONS
from app.schemas import FileResponse

router = APIRouter()


@router.get("/html/{file_name}", response_model=FileResponse)
def render_html(file_name: str, file_type: str) -> FileResponse:
    if file_type not in FILES_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_type} is not supported for this function",
        )

    assigned_base = BASE_FOR_EXTENSION[file_type]
    assigned_extension = FILES_EXTENSIONS[file_type]
    file_path = os.path.join(assigned_base, file_name + assigned_extension)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        html_content = to_html(content, file_type)
        return FileResponse(
            filename=file_name,
            content=html_content,
            filetype=file_type,
        )


@router.post("/markdown/{file_name}", response_model=FileResponse)
def render_markdown(file_name: str, file_type: str) -> FileResponse:
    if file_type not in FILES_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_type} is not supported for this function",
        )

    assigned_base = BASE_FOR_EXTENSION[file_type]
    assigned_extension = FILES_EXTENSIONS[file_type]
    file_path = os.path.join(assigned_base, file_name + assigned_extension)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        md_content = to_markdown(content, file_type)
        return FileResponse(
            filename=file_name,
            content=md_content,
            filetype=file_type,
        )
