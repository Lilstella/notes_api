import os
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_versioning_markdown():
    filename = "testfile_versioning_markdown"

    # Create file
    response = client.post(f"/file/create/{filename}", json={"text": "First version", "filetype": "markdown"})

    # Actualize file
    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "Second version", "filetype": "markdown"})

    time.sleep(1)
    response = client.put(f"/file/edit/{filename}", json={"text": "Third version", "filetype": "markdown"})

    # Verify amount versions
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "markdown"})
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert len(versions) == 2

    # Verify content of versions
    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[0]}", params={"file_type": "markdown"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "First version"

    response = client.request(method="GET", url=f"/file/{filename}/versions/{versions[1]}", params={"file_type": "markdown"})
    assert response.status_code == 200
    content = response.json()["content"]
    assert content == "Second version"

    # Erase file
    response = client.request(method="DELETE", url=f"/file/delete/{filename}", params={"file_type": "markdown"})

    # Verify that versions are deleted
    response = client.request(method="GET", url=f"/file/{filename}/versions", params={"file_type": "markdown"})
    assert response.status_code == 200
    assert response.json()["versions"] == []
