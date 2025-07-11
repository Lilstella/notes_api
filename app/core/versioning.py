import os
from datetime import datetime as dt
from app.constants import VERSION_BASE_DIR

os.makedirs(VERSION_BASE_DIR, exist_ok=True)

def save_version(filename: str, content: str):
    date = dt.now().strftime("%Y%m%d_%H%M%S")
    
    version_directory = os.path.join(VERSION_BASE_DIR, filename)
    os.makedirs(version_directory, exist_ok=True)

    version_path = os.path.join(version_directory, f"{date}.md")

    with open(version_path, "w", encoding="utf-8") as file:
        file.write(content)

    return version_path

def list_versions(filename: str):
    directory = os.path.join(VERSION_BASE_DIR, filename)
    if not os.path.exists(directory):
        return []
    return sorted(os.listdir(directory))

def read_version(filename: str, version: str):
    version_path = os.path.join(VERSION_BASE_DIR, filename, version)
    if not os.path.exists(version_path):
        raise FileNotFoundError(f"Version {version} not found for file {filename}")
    with open(version_path, "r", encoding="utf-8") as file:
        return file.read()

def delete_versions(filename: str):
    directory = os.path.join(VERSION_BASE_DIR, filename)
    if os.path.exists(directory):
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        os.rmdir(directory)
