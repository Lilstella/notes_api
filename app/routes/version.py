from fastapi import APIRouter, HTTPException
from app.schemas import FileVersionResponse, FileVersionsResponse
from app.core.versioning import list_versions, read_version

router = APIRouter()


@router.get("/{file_name}/versions")
def get_file_versions(file_name: str, file_type: str) -> FileVersionsResponse:
    list_of_versions = list_versions(file_name, file_type)
    return FileVersionsResponse(filename=file_name, versions=list_of_versions)


@router.get("/{file_name}/versions/{version}")
def get_file_version(
    file_name: str, version: str, file_type: str
) -> FileVersionResponse:
    try:
        content = read_version(file_name, version, file_type)
        return FileVersionResponse(filename=file_name, version=version, content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Version not found")
