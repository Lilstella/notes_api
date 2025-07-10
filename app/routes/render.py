import os
from fastapi import APIRouter, HTTPException
from app.core.rendering import markdown_to_html, csv_to_markdown
from app.schemas import HtmlResponse, MarkdownResponse

router = APIRouter()

@router.get("/html/{file_name}", response_model=HtmlResponse)
def render_html(file_name: str):
    file_path = f"storage/markdown/{file_name}.md"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        html_content = markdown_to_html(content)
        return HtmlResponse(
            filename=file_name,
            content=html_content,
        )

@router.post("/csv/{file_name}", response_model=MarkdownResponse)
def render_csv(file_name: str):
    file_path = f"storage/csv/{file_name}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        md_content = csv_to_markdown(content)
        return MarkdownResponse(
            filename=file_name,
            content=md_content,
        )
