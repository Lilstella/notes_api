import os
from fastapi import APIRouter, HTTPException
from app.models.schemas import MarkdownContent, MarkdownResponse
from app.core.constants import MARKDOWN_BASE_DIR

os.makedirs(MARKDOWN_BASE_DIR, exist_ok=True)
router = APIRouter()


def get_markdown_file_path(filename: str) -> str:
    return os.path.join(MARKDOWN_BASE_DIR, filename)


@router.get("/{filename}", response_model=MarkdownResponse)
def get_markdown(filename: str):
    file_path = get_markdown_file_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return MarkdownResponse(
            filename=filename,
            content=content
        )

 
@router.post("/{filename}")
def create_markdown(filename: str, content: MarkdownContent):
    file_path = get_markdown_file_path(filename)

    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File already exists")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content.text)

    return {"message": "File created successfully"}
    

@router.put("/{filename}")
def update_markdown(filename: str, content: MarkdownContent):
    file_path = get_markdown_file_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content.text)

    return {"message": "File updated successfully"}


@router.delete("/{filename}")
def delete_markdown(filename: str):
    file_path = get_markdown_file_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)

    return {"message": "File deleted successfully"}
