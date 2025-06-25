from pydantic import BaseModel

class MarkdownContent(BaseModel):
    text: str

class MarkdownResponse(BaseModel):
    filename: str
    content: str
