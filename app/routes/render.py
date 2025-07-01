from fastapi import APIRouter
from app.core.rendering import markdown_to_html, csv_to_markdown
from app.schemas import MarkdownContent, CsvContent

router = APIRouter()

@router.post("/html")
def render_html(content: MarkdownContent):
    html_content = markdown_to_html(content.text)
    return {"html": html_content}

@router.post("/csv")
def render_csv(content: CsvContent):
    markdown_content = csv_to_markdown(content.text)
    return {"markdown": markdown_content}