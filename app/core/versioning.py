import os
from datetime import datetime as dt
from app.constants import VERSION_DIRS, FILES_EXTENSIONS


def save_version(filename: str, content: str, file_type: str) -> str:
    assigned_version_base = VERSION_DIRS[file_type]
    assigned_extension = FILES_EXTENSIONS[file_type]
    date = dt.now().strftime("%Y%m%d_%H%M%S")

    if not os.path.exists(assigned_version_base):
        os.makedirs(assigned_version_base)

    version_file_directory = os.path.join(assigned_version_base, filename)
    os.makedirs(version_file_directory, exist_ok=True)

    version_path = os.path.join(version_file_directory, date + assigned_extension)

    with open(version_path, "w", encoding="utf-8") as file:
        file.write(content)
        return version_path


def list_versions(filename: str, file_type: str) -> list[str]:
    directory = os.path.join(VERSION_DIRS[file_type], filename)
    if not os.path.exists(directory):
        return []
    return sorted(os.listdir(directory))


def read_version(filename: str, version: str, file_type: str) -> str:
    version_path = os.path.join(VERSION_DIRS[file_type], filename, version)

    if not os.path.exists(version_path):
        raise FileNotFoundError(f"Version {version} not found for file {filename}")

    with open(version_path, "r", encoding="utf-8") as file:
        return file.read()


def delete_versions(filename: str, file_type: str) -> None:
    directory = os.path.join(VERSION_DIRS[file_type], filename)

    if os.path.exists(directory):
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        os.rmdir(directory)
