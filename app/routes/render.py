from fastapi import APIRouter
from app.core.render import markdown_to_html
from app.models.schemas import MarkdownContent

router = APIRouter()

@router.post("/html")
def render_html(content: MarkdownContent):
    html_content = markdown_to_html(content.text)
    return {"html": html_content}
