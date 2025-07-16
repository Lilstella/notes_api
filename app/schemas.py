from pydantic import BaseModel, constr
from typing import List


class ImportFileRequest(BaseModel):
    file_path: constr(min_length=1)  # type: ignore[valid-type]


class MarkdownContent(BaseModel):
    text: str


class MarkdownResponse(BaseModel):
    filename: str
    content: str


class MarkdownVersionsResponse(BaseModel):
    filename: str
    versions: List[str]


class MarkdownVersionResponse(BaseModel):
    filename: str
    version: str
    content: str


class CsvContent(BaseModel):
    text: str


class CsvResponse(BaseModel):
    filename: str
    content: str


class HtmlResponse(BaseModel):
    filename: str
    content: str
