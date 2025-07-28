from pydantic import BaseModel, constr
from typing import List


class ImportFileRequest(BaseModel):
    file_path: constr(min_length=1)  # type: ignore[valid-type]


class FileRequest(BaseModel):
    text: str
    filetype: str


class FileResponse(BaseModel):
    filename: str
    content: str
    filetype: str


class FileVersionsResponse(BaseModel):
    filename: str
    versions: List[str]


class FileVersionResponse(BaseModel):
    filename: str
    version: str
    content: str
