from fastapi import APIRouter
from markdown import markdown as md
from app.models.schemas import MarkdownContent

router = APIRouter()

@router.post("/html")
def render_html(content: MarkdownContent):
    html_content = md(content.text)
    return {"html": html_content}
