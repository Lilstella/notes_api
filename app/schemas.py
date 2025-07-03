from pydantic import BaseModel

class MarkdownContent(BaseModel):
    text: str

class MarkdownResponse(BaseModel):
    filename: str
    content: str

class CsvContent(BaseModel):
    text: str

class CsvResponse(BaseModel):
    filename: str
    content: str

class HtmlResponse(BaseModel):
    filename: str
    content: str
